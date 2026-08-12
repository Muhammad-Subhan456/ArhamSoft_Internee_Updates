import { useCallback, useState } from "react";
import Login from "./pages/Login";
import Notes from "./pages/Notes";
import Categories from "./pages/Categories";
import AdminNotes from "./pages/AdminNotes";
import { getToken } from "./services/api";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(() => Boolean(getToken()));
  const [page, setPage] = useState("notes");

  const handleLoginSuccess = useCallback(() => {
    setIsAuthenticated(true);
    setPage("notes");
  }, []);

  const handleLogout = useCallback(() => {
    setIsAuthenticated(false);
    setPage("notes");
  }, []);

  if (!isAuthenticated) {
    return <Login onLoginSuccess={handleLoginSuccess} />;
  }

  if (page === "categories") {
    return (
      <Categories
        currentPage={page}
        onNavigate={setPage}
        onLogout={handleLogout}
      />
    );
  }

  if (page === "admin") {
    return (
      <AdminNotes
        currentPage={page}
        onNavigate={setPage}
        onLogout={handleLogout}
      />
    );
  }

  return (
    <Notes
      currentPage={page}
      onNavigate={setPage}
      onLogout={handleLogout}
    />
  );
}

export default App;
