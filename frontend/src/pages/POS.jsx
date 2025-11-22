import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Button, Badge, Modal, Form, Alert } from 'react-bootstrap';
import { productsAPI, categoriesAPI, ordersAPI } from '../services/api';
import { toast } from 'react-toastify';
import { FiShoppingCart, FiPlus, FiMinus, FiTrash2, FiCheck } from 'react-icons/fi';

const POS = () => {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [cart, setCart] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [orderType, setOrderType] = useState('DINE_IN');
  const [paymentMethod, setPaymentMethod] = useState('CASH');
  const [showPaymentModal, setShowPaymentModal] = useState(false);
  const [showReceipt, setShowReceipt] = useState(false);
  const [currentOrder, setCurrentOrder] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadCategories();
    loadProducts();
  }, []);

  const loadCategories = async () => {
    try {
      const response = await categoriesAPI.getAll();
      setCategories(response.data);
    } catch (error) {
      toast.error('Failed to load categories');
    }
  };

  const loadProducts = async () => {
    try {
      const params = {
        available_only: true,
        category_id: selectedCategory,
        search: searchTerm,
      };
      const response = await productsAPI.getAll(params);
      setProducts(response.data.items || []);
    } catch (error) {
      toast.error('Failed to load products');
    }
  };

  useEffect(() => {
    loadProducts();
  }, [selectedCategory, searchTerm]);

  const addToCart = (product) => {
    const existingItem = cart.find((item) => item.id === product.id);
    if (existingItem) {
      if (existingItem.quantity >= product.stock_qty) {
        toast.warning('Insufficient stock');
        return;
      }
      setCart(
        cart.map((item) =>
          item.id === product.id ? { ...item, quantity: item.quantity + 1 } : item
        )
      );
    } else {
      if (product.stock_qty <= 0) {
        toast.warning('Product out of stock');
        return;
      }
      setCart([...cart, { ...product, quantity: 1 }]);
    }
  };

  const updateQuantity = (productId, delta) => {
    setCart(
      cart
        .map((item) =>
          item.id === productId
            ? { ...item, quantity: Math.max(1, item.quantity + delta) }
            : item
        )
        .filter((item) => item.quantity > 0)
    );
  };

  const removeFromCart = (productId) => {
    setCart(cart.filter((item) => item.id !== productId));
  };

  const calculateSubtotal = () => {
    return cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
  };

  const calculateTax = () => {
    return calculateSubtotal() * 0.05; // 5% tax
  };

  const calculateTotal = () => {
    return calculateSubtotal() + calculateTax();
  };

  const handleCheckout = () => {
    if (cart.length === 0) {
      toast.warning('Cart is empty');
      return;
    }
    setShowPaymentModal(true);
  };

  const handlePayment = async () => {
    setLoading(true);
    try {
      const orderData = {
        order_type: orderType,
        payment_method: paymentMethod,
        items: cart.map((item) => ({
          product_id: item.id,
          quantity: item.quantity,
        })),
      };

      const response = await ordersAPI.create(orderData);
      setCurrentOrder(response.data.order);
      setCart([]);
      setShowPaymentModal(false);
      setShowReceipt(true);
      toast.success('Order placed successfully!');
      loadProducts(); // Refresh product stock
    } catch (error) {
      toast.error(error.response?.data?.error || 'Failed to place order');
    } finally {
      setLoading(false);
    }
  };

  const filteredProducts = products.filter((product) => {
    if (selectedCategory && product.category_id !== selectedCategory) return false;
    if (searchTerm && !product.name.toLowerCase().includes(searchTerm.toLowerCase())) return false;
    return true;
  });

  return (
    <Container fluid>
      <Row>
        <Col md={8}>
          <Card className="mb-3">
            <Card.Header className="d-flex justify-content-between align-items-center">
              <h5 className="mb-0">Products</h5>
              <Form.Control
                type="text"
                placeholder="Search products..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                style={{ width: '300px' }}
              />
            </Card.Header>
            <Card.Body>
              <div className="mb-3">
                <Button
                  variant={selectedCategory === null ? 'primary' : 'outline-primary'}
                  className="me-2 mb-2"
                  onClick={() => setSelectedCategory(null)}
                >
                  All
                </Button>
                {categories.map((category) => (
                  <Button
                    key={category.id}
                    variant={selectedCategory === category.id ? 'primary' : 'outline-primary'}
                    className="me-2 mb-2"
                    onClick={() => setSelectedCategory(category.id)}
                  >
                    {category.name}
                  </Button>
                ))}
              </div>

              <Row>
                {filteredProducts.map((product) => (
                  <Col key={product.id} md={4} className="mb-3">
                    <Card
                      className="h-100"
                      style={{ cursor: product.stock_qty > 0 ? 'pointer' : 'not-allowed' }}
                      onClick={() => product.stock_qty > 0 && addToCart(product)}
                    >
                      <Card.Body>
                        <Card.Title>{product.name}</Card.Title>
                        <Card.Text className="text-muted">{product.description}</Card.Text>
                        <div className="d-flex justify-content-between align-items-center">
                          <strong>${product.price.toFixed(2)}</strong>
                          <Badge bg={product.stock_qty > 0 ? 'success' : 'danger'}>
                            Stock: {product.stock_qty}
                          </Badge>
                        </div>
                      </Card.Body>
                    </Card>
                  </Col>
                ))}
              </Row>
            </Card.Body>
          </Card>
        </Col>

        <Col md={4}>
          <Card>
            <Card.Header>
              <h5 className="mb-0">
                <FiShoppingCart className="me-2" />
                Cart
              </h5>
            </Card.Header>
            <Card.Body>
              {cart.length === 0 ? (
                <p className="text-muted text-center py-4">Cart is empty</p>
              ) : (
                <>
                  {cart.map((item) => (
                    <div key={item.id} className="d-flex justify-content-between align-items-center mb-2 pb-2 border-bottom">
                      <div className="flex-grow-1">
                        <strong>{item.name}</strong>
                        <br />
                        <small className="text-muted">${item.price.toFixed(2)} each</small>
                      </div>
                      <div className="d-flex align-items-center">
                        <Button
                          variant="outline-secondary"
                          size="sm"
                          onClick={() => updateQuantity(item.id, -1)}
                        >
                          <FiMinus />
                        </Button>
                        <span className="mx-2">{item.quantity}</span>
                        <Button
                          variant="outline-secondary"
                          size="sm"
                          onClick={() => updateQuantity(item.id, 1)}
                          disabled={item.quantity >= item.stock_qty}
                        >
                          <FiPlus />
                        </Button>
                        <Button
                          variant="outline-danger"
                          size="sm"
                          className="ms-2"
                          onClick={() => removeFromCart(item.id)}
                        >
                          <FiTrash2 />
                        </Button>
                      </div>
                    </div>
                  ))}
                  <hr />
                  <div className="d-flex justify-content-between mb-2">
                    <span>Subtotal:</span>
                    <span>${calculateSubtotal().toFixed(2)}</span>
                  </div>
                  <div className="d-flex justify-content-between mb-2">
                    <span>Tax (5%):</span>
                    <span>${calculateTax().toFixed(2)}</span>
                  </div>
                  <div className="d-flex justify-content-between mb-3">
                    <strong>Total:</strong>
                    <strong>${calculateTotal().toFixed(2)}</strong>
                  </div>
                  <Form.Group className="mb-3">
                    <Form.Label>Order Type</Form.Label>
                    <Form.Select
                      value={orderType}
                      onChange={(e) => setOrderType(e.target.value)}
                    >
                      <option value="DINE_IN">Dine In</option>
                      <option value="TAKEAWAY">Takeaway</option>
                    </Form.Select>
                  </Form.Group>
                  <Button
                    variant="primary"
                    className="w-100"
                    onClick={handleCheckout}
                  >
                    <FiCheck className="me-2" />
                    Checkout
                  </Button>
                </>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Payment Modal */}
      <Modal show={showPaymentModal} onHide={() => setShowPaymentModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Payment</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div className="mb-3">
            <strong>Total: ${calculateTotal().toFixed(2)}</strong>
          </div>
          <Form.Group className="mb-3">
            <Form.Label>Payment Method</Form.Label>
            <Form.Select
              value={paymentMethod}
              onChange={(e) => setPaymentMethod(e.target.value)}
            >
              <option value="CASH">Cash</option>
              <option value="CARD">Card</option>
              <option value="QR">QR Code</option>
            </Form.Select>
          </Form.Group>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowPaymentModal(false)}>
            Cancel
          </Button>
          <Button variant="primary" onClick={handlePayment} disabled={loading}>
            {loading ? 'Processing...' : 'Confirm Payment'}
          </Button>
        </Modal.Footer>
      </Modal>

      {/* Receipt Modal */}
      <Modal show={showReceipt} onHide={() => setShowReceipt(false)} size="lg">
        <Modal.Header closeButton>
          <Modal.Title>Receipt</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {currentOrder && (
            <div className="receipt-container">
              <div className="receipt-header">
                <h4>Coffee Shop</h4>
                <p>Order #{currentOrder.order_number}</p>
                <p>{new Date(currentOrder.created_at).toLocaleString()}</p>
              </div>
              <div className="mb-3">
                {currentOrder.items.map((item) => (
                  <div key={item.id} className="receipt-item">
                    <div>
                      <strong>{item.product_name}</strong>
                      <br />
                      <small>
                        {item.quantity} x ${item.unit_price.toFixed(2)}
                      </small>
                    </div>
                    <div>${item.total_price.toFixed(2)}</div>
                  </div>
                ))}
              </div>
              <div className="receipt-total">
                <div className="d-flex justify-content-between">
                  <span>Subtotal:</span>
                  <span>${currentOrder.subtotal.toFixed(2)}</span>
                </div>
                <div className="d-flex justify-content-between">
                  <span>Tax:</span>
                  <span>${currentOrder.tax.toFixed(2)}</span>
                </div>
                <div className="d-flex justify-content-between">
                  <strong>Total:</strong>
                  <strong>${currentOrder.total.toFixed(2)}</strong>
                </div>
                <div className="mt-2">
                  <small>Payment: {currentOrder.payment_method}</small>
                  <br />
                  <small>Type: {currentOrder.order_type.replace('_', ' ')}</small>
                </div>
              </div>
            </div>
          )}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowReceipt(false)}>
            Close
          </Button>
          <Button variant="primary" onClick={() => window.print()}>
            Print
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );
};

export default POS;

