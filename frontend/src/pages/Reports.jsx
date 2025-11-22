import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Table, Form, Button } from 'react-bootstrap';
import { reportsAPI } from '../services/api';
import { toast } from 'react-toastify';
import { useAuth } from '../contexts/AuthContext';

const Reports = () => {
  const { isAdmin } = useAuth();
  const [startDate, setStartDate] = useState(new Date().toISOString().split('T')[0]);
  const [endDate, setEndDate] = useState(new Date().toISOString().split('T')[0]);
  const [salesReport, setSalesReport] = useState(null);
  const [itemReport, setItemReport] = useState(null);
  const [cashierReport, setCashierReport] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadReports();
  }, []);

  const loadReports = async () => {
    setLoading(true);
    try {
      const params = { start_date: startDate, end_date: endDate };
      
      // Always fetch sales and item reports
      const promises = [
        reportsAPI.getSales(params),
        reportsAPI.getItemSales(params),
      ];
      
      // Only fetch cashier report if user is admin
      if (isAdmin()) {
        promises.push(reportsAPI.getCashierReport(params));
      }
      
      // Use allSettled so one failure doesn't block others
      const results = await Promise.allSettled(promises);
      
      // Set sales report
      if (results[0].status === 'fulfilled') {
        setSalesReport(results[0].value.data);
      } else {
        console.error('Failed to load sales report:', results[0].reason);
      }
      
      // Set item report
      if (results[1].status === 'fulfilled') {
        setItemReport(results[1].value.data);
      } else {
        console.error('Failed to load item sales report:', results[1].reason);
      }
      
      // Only set cashier report if it was fetched and successful
      if (isAdmin()) {
        if (results[2]?.status === 'fulfilled') {
          setCashierReport(results[2].value.data);
        } else {
          setCashierReport(null);
          // Only log error, don't show toast for 403 (expected for non-admins)
          if (results[2]?.reason?.response?.status !== 403) {
            console.error('Failed to load cashier report:', results[2]?.reason);
          }
        }
      } else {
        setCashierReport(null);
      }
      
      // Show error toast if any critical reports failed
      const criticalFailures = results.slice(0, 2).filter(r => r.status === 'rejected');
      if (criticalFailures.length > 0) {
        toast.error('Failed to load some reports');
      }
    } catch (error) {
      console.error('Error loading reports:', error);
      toast.error('Failed to load reports');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    loadReports();
  };

  return (
    <Container fluid>
      <Card className="mb-3">
        <Card.Header>
          <h5 className="mb-0">Reports</h5>
        </Card.Header>
        <Card.Body>
          <Form onSubmit={handleSubmit}>
            <Row>
              <Col md={4}>
                <Form.Group className="mb-3">
                  <Form.Label>Start Date</Form.Label>
                  <Form.Control
                    type="date"
                    value={startDate}
                    onChange={(e) => setStartDate(e.target.value)}
                  />
                </Form.Group>
              </Col>
              <Col md={4}>
                <Form.Group className="mb-3">
                  <Form.Label>End Date</Form.Label>
                  <Form.Control
                    type="date"
                    value={endDate}
                    onChange={(e) => setEndDate(e.target.value)}
                  />
                </Form.Group>
              </Col>
              <Col md={4} className="d-flex align-items-end">
                <Button variant="primary" type="submit" disabled={loading}>
                  {loading ? 'Loading...' : 'Generate Report'}
                </Button>
              </Col>
            </Row>
          </Form>
        </Card.Body>
      </Card>

      <Row>
        <Col md={12}>
          <Card className="mb-3">
            <Card.Header>
              <h5 className="mb-0">Sales Summary</h5>
            </Card.Header>
            <Card.Body>
              {salesReport && (
                <div>
                  <Row className="mb-3">
                    <Col md={3}>
                      <strong>Total Orders:</strong> {salesReport.summary.total_orders}
                    </Col>
                    <Col md={3}>
                      <strong>Total Revenue:</strong> ${salesReport.summary.total_revenue.toFixed(2)}
                    </Col>
                    <Col md={3}>
                      <strong>Total Tax:</strong> ${salesReport.summary.total_tax.toFixed(2)}
                    </Col>
                    <Col md={3}>
                      <strong>Subtotal:</strong> ${salesReport.summary.total_subtotal.toFixed(2)}
                    </Col>
                  </Row>
                </div>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Row>
        <Col md={isAdmin() ? 6 : 12}>
          <Card className="mb-3">
            <Card.Header>
              <h5 className="mb-0">Item Sales</h5>
            </Card.Header>
            <Card.Body>
              {itemReport && (
                <Table striped bordered hover size="sm">
                  <thead>
                    <tr>
                      <th>Product</th>
                      <th>Quantity</th>
                      <th>Revenue</th>
                    </tr>
                  </thead>
                  <tbody>
                    {itemReport.items.map((item) => (
                      <tr key={item.product_id}>
                        <td>{item.product_name}</td>
                        <td>{item.total_quantity}</td>
                        <td>${item.total_revenue.toFixed(2)}</td>
                      </tr>
                    ))}
                  </tbody>
                </Table>
              )}
            </Card.Body>
          </Card>
        </Col>
        {isAdmin() && (
          <Col md={6}>
            <Card className="mb-3">
              <Card.Header>
                <h5 className="mb-0">Cashier Performance</h5>
              </Card.Header>
              <Card.Body>
                {cashierReport && (
                  <Table striped bordered hover size="sm">
                    <thead>
                      <tr>
                        <th>Cashier</th>
                        <th>Orders</th>
                        <th>Revenue</th>
                      </tr>
                    </thead>
                    <tbody>
                      {cashierReport.cashiers.map((cashier) => (
                        <tr key={cashier.cashier_id}>
                          <td>{cashier.cashier_name}</td>
                          <td>{cashier.total_orders}</td>
                          <td>${cashier.total_revenue.toFixed(2)}</td>
                        </tr>
                      ))}
                    </tbody>
                  </Table>
                )}
              </Card.Body>
            </Card>
          </Col>
        )}
      </Row>
    </Container>
  );
};

export default Reports;

