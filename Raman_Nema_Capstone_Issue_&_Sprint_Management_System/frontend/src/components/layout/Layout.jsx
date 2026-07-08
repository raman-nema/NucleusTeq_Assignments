import Sidebar from "./Sidebar";
import "../../styles/layout-styles";

function Layout({ children }) {
  return (
    <div className="app-layout">
      <Sidebar />
      <main className="app-content">{children}</main>
    </div>
  );
}

export default Layout;
