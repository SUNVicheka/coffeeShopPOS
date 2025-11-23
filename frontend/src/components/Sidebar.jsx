import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { FiLogOut, FiShoppingCart, FiPackage, FiFileText, FiBarChart, FiUsers, FiMenu, FiX } from 'react-icons/fi';
import './Sidebar.css';

const Sidebar = ({ onLogout, onToggle, isOpen }) => {
  const { user, isAdmin } = useAuth();
  const location = useLocation();

  const handleToggle = () => {
    onToggle?.(!isOpen);
  };

  const isActive = (path) => {
    return location.pathname === path;
  };

  const navItems = [
    { path: '/pos', label: 'POS', icon: FiShoppingCart },
    { path: '/products', label: 'Products', icon: FiPackage },
    { path: '/orders', label: 'Orders', icon: FiFileText },
    { path: '/reports', label: 'Reports', icon: FiBarChart },
  ];

  return (
    <>
      {/* Sidebar */}
      <div className={`sidebar ${isOpen ? 'open' : 'closed'}`}>
        {/* Sidebar Header - Only Toggle Button */}
        <div className="sidebar-header">
          <button className="sidebar-toggle" onClick={handleToggle}>
            {isOpen ? <FiX size={20} /> : <FiMenu size={20} />}
          </button>
        </div>

        {/* Navigation Items */}
        <nav className="sidebar-nav">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`nav-item ${isActive(item.path) ? 'active' : ''}`}
                title={item.label}
              >
                <Icon size={20} />
                {isOpen && <span>{item.label}</span>}
              </Link>
            );
          })}

          {isAdmin() && (
            <Link
              to="/users"
              className={`nav-item ${isActive('/users') ? 'active' : ''}`}
              title="Users"
            >
              <FiUsers size={20} />
              {isOpen && <span>Users</span>}
            </Link>
          )}
        </nav>

        {/* Sidebar Footer */}
        <div className="sidebar-footer">
          {isOpen && (
            <div className="user-info">
              <div className="user-avatar">
                {user?.full_name?.charAt(0).toUpperCase()}
              </div>
              <div className="user-details">
                <p className="user-name">{user?.full_name || user?.username}</p>
                <p className="user-role">{user?.role}</p>
              </div>
            </div>
          )}
          <button className="logout-btn" onClick={onLogout} title="Logout">
            <FiLogOut size={20} />
            {isOpen && <span>Logout</span>}
          </button>
        </div>
      </div>

      {/* Overlay for mobile */}
      {isOpen && (
        <div className="sidebar-overlay" onClick={handleToggle} />
      )}
    </>
  );
};

export default Sidebar;
