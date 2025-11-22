import React from 'react';
import { Outlet, Link, useNavigate, useLocation } from 'react-router-dom';
import { Navbar, Nav, Container, Button } from 'react-bootstrap';
import { useAuth } from '../contexts/AuthContext';
import { FiLogOut, FiShoppingCart, FiPackage, FiFileText, FiBarChart, FiUsers } from 'react-icons/fi';

const Layout = () => {
  const { user, logout, isAdmin } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <div className="d-flex flex-column" style={{ minHeight: '100vh' }}>
      <Navbar bg="dark" variant="dark" expand="lg" className="mb-3">
        <Container fluid>
          <Navbar.Brand>
            <FiShoppingCart className="me-2" />
            Coffee Shop POS
          </Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="me-auto">
              <Nav.Link as={Link} to="/pos" active={isActive('/pos')}>
                <FiShoppingCart className="me-1" />
                POS
              </Nav.Link>
              <Nav.Link as={Link} to="/products" active={isActive('/products')}>
                <FiPackage className="me-1" />
                Products
              </Nav.Link>
              <Nav.Link as={Link} to="/orders" active={isActive('/orders')}>
                <FiFileText className="me-1" />
                Orders
              </Nav.Link>
              <Nav.Link as={Link} to="/reports" active={isActive('/reports')}>
                <FiBarChart className="me-1" />
                Reports
              </Nav.Link>
              {isAdmin() && (
                <Nav.Link as={Link} to="/users" active={isActive('/users')}>
                  <FiUsers className="me-1" />
                  Users
                </Nav.Link>
              )}
            </Nav>
            <Nav>
              <Navbar.Text className="me-3">
                Welcome, <strong>{user?.full_name || user?.username}</strong>
                {isAdmin() && <span className="badge bg-primary ms-2">Admin</span>}
              </Navbar.Text>
              <Button variant="outline-light" size="sm" onClick={handleLogout}>
                <FiLogOut className="me-1" />
                Logout
              </Button>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>

      <Container fluid className="flex-grow-1 pb-4">
        <Outlet />
      </Container>
    </div>
  );
};

export default Layout;

