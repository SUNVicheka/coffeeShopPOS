import React, { useState, useEffect } from 'react';
import { Container, Card, Table, Badge, Button, Modal } from 'react-bootstrap';
import { ordersAPI } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import { toast } from 'react-toastify';
import { FiEye, FiX } from 'react-icons/fi';
import './Orders.css';

const Orders = () => {
  const { isAdmin } = useAuth();
  const [orders, setOrders] = useState([]);
  const [selectedOrder, setSelectedOrder] = useState(null);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    loadOrders();
  }, []);

  const loadOrders = async () => {
    try {
      const response = await ordersAPI.getAll({ per_page: 50 });
      setOrders(response.data.items || []);
    } catch (error) {
      toast.error('Failed to load orders');
    }
  };

  const handleCancel = async (orderId) => {
    if (!window.confirm('Are you sure you want to cancel this order?')) return;
    try {
      await ordersAPI.cancel(orderId);
      toast.success('Order cancelled successfully');
      loadOrders();
    } catch (error) {
      toast.error(error.response?.data?.error || 'Failed to cancel order');
    }
  };

  const viewOrder = async (orderId) => {
    try {
      const response = await ordersAPI.getById(orderId);
      setSelectedOrder(response.data);
      setShowModal(true);
    } catch (error) {
      toast.error('Failed to load order details');
    }
  };

  return (
    <Container fluid>
      <Card>
        <Card.Header>
          <h5 className="mb-0">Orders</h5>
        </Card.Header>
        <Card.Body>
          <Table striped bordered hover responsive>
            <thead>
              <tr>
                <th>Order Number</th>
                <th>Date</th>
                <th>Cashier</th>
                <th>Type</th>
                <th>Payment</th>
                <th>Total</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {orders.map((order) => (
                <tr key={order.id}>
                  <td>{order.order_number}</td>
                  <td>{new Date(order.created_at).toLocaleString()}</td>
                  <td>{order.cashier_name}</td>
                  <td>
                    <Badge bg="info">{order.order_type.replace('_', ' ')}</Badge>
                  </td>
                  <td>{order.payment_method}</td>
                  <td>${order.total.toFixed(2)}</td>
                  <td>
                    <Badge bg={order.status === 'COMPLETED' ? 'success' : 'danger'}>
                      {order.status}
                    </Badge>
                  </td>
                  <td>
                    <Button
                      variant="outline-primary"
                      size="sm"
                      className="me-2"
                      onClick={() => viewOrder(order.id)}
                    >
                      <FiEye />
                    </Button>
                    {isAdmin() && order.status === 'COMPLETED' && (
                      <Button
                        variant="outline-danger"
                        size="sm"
                        onClick={() => handleCancel(order.id)}
                      >
                        <FiX />
                      </Button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>
        </Card.Body>
      </Card>

      {/* Order Detail Modal */}
      <Modal show={showModal} onHide={() => setShowModal(false)} size="lg">
        <Modal.Header closeButton>
          <Modal.Title>Order #{selectedOrder?.order_number}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {selectedOrder && (
            <div>
              <p><strong>Date:</strong> {new Date(selectedOrder.created_at).toLocaleString()}</p>
              <p><strong>Cashier:</strong> {selectedOrder.cashier_name}</p>
              <p><strong>Type:</strong> {selectedOrder.order_type.replace('_', ' ')}</p>
              <p><strong>Payment:</strong> {selectedOrder.payment_method}</p>
              <hr />
              <h6>Items:</h6>
              <Table striped bordered size="sm">
                <thead>
                  <tr>
                    <th>Product</th>
                    <th>Quantity</th>
                    <th>Price</th>
                    <th>Total</th>
                  </tr>
                </thead>
                <tbody>
                  {selectedOrder.items.map((item) => (
                    <tr key={item.id}>
                      <td>{item.product_name}</td>
                      <td>{item.quantity}</td>
                      <td>${item.unit_price.toFixed(2)}</td>
                      <td>${item.total_price.toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </Table>
              <hr />
              <div className="d-flex justify-content-between">
                <strong>Subtotal:</strong>
                <strong>${selectedOrder.subtotal.toFixed(2)}</strong>
              </div>
              <div className="d-flex justify-content-between">
                <strong>Tax:</strong>
                <strong>${selectedOrder.tax.toFixed(2)}</strong>
              </div>
              <div className="d-flex justify-content-between">
                <strong>Total:</strong>
                <strong>${selectedOrder.total.toFixed(2)}</strong>
              </div>
            </div>
          )}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowModal(false)}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );
};

export default Orders;

