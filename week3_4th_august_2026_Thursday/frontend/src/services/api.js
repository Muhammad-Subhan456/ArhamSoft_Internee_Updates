const API_URL = import.meta.env.VITE_API_URL;

const TOKEN_KEY = "access_token";

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token) {
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
}

export class ApiError extends Error {
  constructor(message, status, detail) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.detail = detail;
  }
}

async function parseErrorBody(response) {
  const contentType = response.headers.get("content-type") || "";

  if (!contentType.includes("application/json")) {
    const text = await response.text();
    return text || `Request failed: ${response.status}`;
  }

  const data = await response.json();

  if (typeof data?.detail === "string") {
    return data.detail;
  }

  if (Array.isArray(data?.detail)) {
    return data.detail
      .map((item) => item.msg || JSON.stringify(item))
      .join(", ");
  }

  return data?.message || `Request failed: ${response.status}`;
}

async function request(path, options = {}) {
  const headers = {
    ...(options.headers || {}),
  };

  if (options.body !== undefined && !headers["Content-Type"]) {
    headers["Content-Type"] = "application/json";
  }

  const token = getToken();
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  let response;

  try {
    response = await fetch(`${API_URL}${path}`, {
      ...options,
      headers,
    });
  } catch {
    throw new ApiError(
      "Unable to reach the server. Check that the API is running.",
      0,
      "Network error",
    );
  }

  if (!response.ok) {
    const detail = await parseErrorBody(response);
    let message = detail;

    if (response.status === 401) {
      message =
        detail === "Invalid email or password"
          ? detail
          : "Authentication failed. Please log in again.";
    } else if (response.status === 404) {
      message = detail || "Resource does not exist.";
    }

    throw new ApiError(message, response.status, detail);
  }

  if (response.status === 204) {
    return null;
  }

  const contentType = response.headers.get("content-type") || "";
  if (!contentType.includes("application/json")) {
    return null;
  }

  return response.json();
}

export const api = {
  get(path) {
    return request(path, { method: "GET" });
  },

  post(path, body) {
    return request(path, {
      method: "POST",
      body: JSON.stringify(body),
    });
  },

  put(path, body) {
    return request(path, {
      method: "PUT",
      body: JSON.stringify(body),
    });
  },

  delete(path) {
    return request(path, { method: "DELETE" });
  },
};

export const authApi = {
  login(email, password) {
    return api.post("/api/v1/auth/login", { email, password });
  },

  register(username, email, password) {
    return api.post("/api/v1/auth/register", {
      username,
      email,
      password,
    });
  },
};

export const notesApi = {
  list() {
    return api.get("/api/v1/notes");
  },

  getById(id) {
    return api.get(`/api/v1/notes/${id}`);
  },

  create(payload) {
    return api.post("/api/v1/notes", payload);
  },

  update(id, payload) {
    return api.put(`/api/v1/notes/${id}`, payload);
  },

  remove(id) {
    return api.delete(`/api/v1/notes/${id}`);
  },
};

export const categoriesApi = {
  list() {
    return api.get("/api/v1/categories");
  },

  getById(id) {
    return api.get(`/api/v1/categories/${id}`);
  },

  create(payload) {
    return api.post("/api/v1/categories", payload);
  },

  update(id, payload) {
    return api.put(`/api/v1/categories/${id}`, payload);
  },

  remove(id) {
    return api.delete(`/api/v1/categories/${id}`);
  },
};

export const adminApi = {
  listNotes() {
    return api.get("/api/v1/admin/notes");
  },
};

export function getTokenPayload() {
  const token = getToken();
  if (!token) {
    return null;
  }

  try {
    const payload = token.split(".")[1];
    if (!payload) {
      return null;
    }

    const normalized = payload.replace(/-/g, "+").replace(/_/g, "/");
    const json = atob(normalized.padEnd(Math.ceil(normalized.length / 4) * 4, "="));
    return JSON.parse(json);
  } catch {
    return null;
  }
}

export function getCurrentRole() {
  return getTokenPayload()?.role || null;
}
