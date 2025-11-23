import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, Card, Form, Button, Alert } from 'react-bootstrap';
import { useAuth } from '../contexts/AuthContext';
import { toast } from 'react-toastify';
import { FiLogIn } from 'react-icons/fi';
import './Login.css';

const loginStyles = `
  body { background-color: var(--cream) !important; }
  .login-wrapper { min-height: 100vh !important; display: flex !important; align-items: center !important; justify-content: center !important; background: linear-gradient(135deg, var(--light-yellow), var(--cream)) !important; }
  .card { background: white !important; border: 1px solid var(--border-gray) !important; border-radius: 8px !important; box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important; }
  .form-control { border: 1px solid var(--border-gray) !important; background-color: var(--cream) !important; }
  .form-control:focus { border-color: var(--primary-yellow) !important; box-shadow: 0 0 0 3px rgba(253,185,19,0.1) !important; background-color: white !important; }
  .btn-primary { background: linear-gradient(135deg, var(--primary-yellow), var(--dark-yellow)) !important; border: none !important; color: white !important; }
`;

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const result = await login(username, password);
      if (result.success) {
        toast.success('Login successful!');
        navigate('/pos');
      } else {
        setError(result.error || 'Login failed');
        toast.error(result.error || 'Login failed');
      }
    } catch (err) {
      setError('An error occurred. Please try again.');
      toast.error('An error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <style>{loginStyles}</style>
      <div
        style={{
          minHeight: '100vh',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          background: 'linear-gradient(135deg, var(--light-yellow) 0%, var(--cream) 100%)',
        }}
      >
        <Container style={{ maxWidth: '400px' }}>
          <Card>
            <Card.Body className="p-4">
              <div className="text-center mb-4">
                <FiLogIn size={48} style={{ color: 'var(--primary-yellow)', marginBottom: '12px' }} />
                <h2 className="mb-2" style={{ color: 'var(--text-dark)', fontWeight: 700 }}>Coffee Shop POS</h2>
                <p className="text-muted">Sign in to your account</p>
              </div>

              {error && (
                <Alert variant="danger" dismissible onClose={() => setError('')}>
                  {error}
                </Alert>
              )}

              <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3">
                  <Form.Label>Username</Form.Label>
                  <Form.Control
                    type="text"
                    placeholder="Enter username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                    autoFocus
                  />
                </Form.Group>

                <Form.Group className="mb-3">
                  <Form.Label>Password</Form.Label>
                  <Form.Control
                    type="password"
                    placeholder="Enter password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                  />
                </Form.Group>

                <Button
                  variant="primary"
                  type="submit"
                  className="w-100"
                  disabled={loading}
                >
                  {loading ? 'Signing in...' : 'Sign In'}
                </Button>
              </Form>

              <div className="mt-4 text-center">
                <small className="text-muted">
                  Default credentials:<br />
                  Admin: admin / admin123<br />
                  Cashier: cashier / cashier123
                </small>
              </div>
            </Card.Body>
          </Card>
        </Container>
      </div>
    </>
  );
};

export default Login;

