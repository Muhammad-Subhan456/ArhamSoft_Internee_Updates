import { useState } from "react";
import { authApi, setToken } from "../services/api";
import ErrorMessage from "../components/ErrorMessage";

function Login({ onLoginSuccess }) {
  const [mode, setMode] = useState("login");
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const isRegister = mode === "register";

  function switchMode(nextMode) {
    setMode(nextMode);
    setError("");
    setSuccess("");
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setSuccess("");
    setSubmitting(true);

    try {
      if (isRegister) {
        await authApi.register(username.trim(), email.trim(), password);
        setSuccess("Account created. You can sign in now.");
        setMode("login");
        setPassword("");
        return;
      }

      const data = await authApi.login(email.trim(), password);

      if (!data?.access_token) {
        throw new Error("Login response did not include an access token.");
      }

      setToken(data.access_token);
      onLoginSuccess();
    } catch (err) {
      setError(err.message || (isRegister ? "Sign up failed." : "Login failed."));
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-shell">
        <section className="auth-brand" aria-label="Product branding">
          <p className="brand-name">ArhamSoft Notes</p>
          <h1>{isRegister ? "Create your workspace account" : "Sign in to your workspace"}</h1>
          <p className="auth-support">
            Manage notes securely with your company account.
          </p>
        </section>

        <section className="auth-panel" aria-labelledby="auth-heading">
          <h2 id="auth-heading">{isRegister ? "Sign up" : "Log in"}</h2>
          <p className="panel-subtitle">
            {isRegister
              ? "Register with a username, email, and password"
              : "Use your registered email and password"}
          </p>

          <ErrorMessage message={error} onDismiss={() => setError("")} />

          {success ? (
            <div className="feedback feedback-success" role="status">
              <p>{success}</p>
              <button
                type="button"
                className="feedback-dismiss"
                onClick={() => setSuccess("")}
                aria-label="Dismiss success message"
              >
                Dismiss
              </button>
            </div>
          ) : null}

          <form className="auth-form" onSubmit={handleSubmit}>
            {isRegister ? (
              <div className="form-field">
                <label htmlFor="register-username">Username</label>
                <input
                  id="register-username"
                  name="username"
                  type="text"
                  autoComplete="username"
                  value={username}
                  onChange={(event) => setUsername(event.target.value)}
                  required
                />
              </div>
            ) : null}

            <div className="form-field">
              <label htmlFor="auth-email">Email</label>
              <input
                id="auth-email"
                name="email"
                type="email"
                autoComplete="email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                required
              />
            </div>

            <div className="form-field">
              <label htmlFor="auth-password">Password</label>
              <input
                id="auth-password"
                name="password"
                type="password"
                autoComplete={isRegister ? "new-password" : "current-password"}
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                required
              />
            </div>

            <button
              type="submit"
              className="btn btn-primary btn-block"
              disabled={submitting}
            >
              {submitting
                ? isRegister
                  ? "Creating account..."
                  : "Signing in..."
                : isRegister
                  ? "Create account"
                  : "Sign in"}
            </button>
          </form>

          <p className="auth-switch">
            {isRegister ? "Already have an account?" : "Need an account?"}{" "}
            <button
              type="button"
              className="link-button"
              onClick={() => switchMode(isRegister ? "login" : "register")}
            >
              {isRegister ? "Sign in" : "Sign up"}
            </button>
          </p>
        </section>
      </div>
    </div>
  );
}

export default Login;
