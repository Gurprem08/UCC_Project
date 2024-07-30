import React from "react";
import { Card, Row, Col } from "react-bootstrap";
import NN from '../NN.jpg';
import Dashboard from '../dashboard.png'; // Add an image for the dashboard service
import consulting from '../consulting.jpg'

const ServicePage = () => {
  return (
    <div className="services-container">
      <h1 className="title" style={{margin:'50px', color:"black"}}>Our Services</h1>
      <Row style={{paddingTop:'50px'}}>
        <Col md={6}>
          <Card className="h-100 hover-card">
            <Card.Img variant="top" src= {consulting} />
            <Card.Body>
              <Card.Title style={{fontWeight:'bold', fontSize:'30px'}}>Water Quality Testing & Consultation </Card.Title>
              <Card.Text>
                In addition to our predictive and analytical tools, we offer expert consultation services to help users interpret their water quality data and make informed decisions. Our consultation services include:
              </Card.Text>
              
              <ul >
                <p style={{fontWeight:'bold'}}>Single time Water quality testing and basic consultation.</p>
                <p style={{fontWeight:'bold'}}>Personalized advice on water treatment solutions.</p>
                <p style={{fontWeight:'bold'}}>Parameter specific detailed recommendation.</p>
                
              </ul>
              <Card.Text>
                Our team of experts is always ready to assist you with any queries or concerns, ensuring you get the most out of our services.
              </Card.Text>
            </Card.Body>
          </Card>
        </Col>
        <Col md={6}>
          <Card className="h-100 hover-card">
            <Card.Img variant="top" src= {Dashboard} />
            <Card.Body>
              <Card.Title style={{fontWeight:'bold', fontSize:'30px'}}>Real-Time Visualization</Card.Title>
              <Card.Text>
                Our real-time Tableau dashboard offers users dynamic and interactive visualizations of the water quality data. This enables users to:
              </Card.Text>
              <ul>
                <p style={{fontWeight:'bold', textalign: "left"}}>Monitor changes in water quality parameters over time.</p>
                <p style={{fontWeight:'bold'}}>Identify trends and potential issues promptly.</p>
                <p style={{fontWeight:'bold'}}>Customize the dashboard to focus on specific parameters of interest and location.</p>
                
              </ul>
              <Card.Text>
                The dashboard is designed to be user-friendly, making it easy for both experts and non-experts to understand and utilize the data effectively.
              </Card.Text>
            </Card.Body>
          </Card>
        </Col>
      </Row>
      <Row>
      <h1 className="title" style={{ color:"black", marginRight:'150px'}}>What we do?</h1>
        <Col md={12}>
          <Card className="h-100 hover-card">
            <Card.Img variant="top" src={NN} />
            <Card.Body>
              <Card.Title style={{fontWeight:'bold', fontSize:'30px'}}>Advanced Machine Learning for Water Quality Prediction</Card.Title>
              <Card.Text>
                We utilize an advanced machine learning algorithm, specifically a neural network, trained on a comprehensive groundwater dataset collected from reliable sources.
              </Card.Text>
              <Card.Text>
                Our system predicts key water quality parameters and calculates the overall water quality index (WQI) of samples, helping users understand the potential uses and limitations of their water.
              </Card.Text>
              <Card.Text>
                Our approach leverages easily measurable basic water quality parameters provided by users, including: pH, Electrical Conductivity (EC) (µS/cm), Total Dissolved Solids (TDS) (mg/L), and Temperature (°C).
              </Card.Text>
              <Card.Text>
                Using these inputs, our neural network predicts additional parameters such as: Carbonate (CO<sub>3</sub>), Chloride (Cl), Sulfate (SO<sub>4</sub>), Total Hardness (TH), Calcium (Ca), Magnesium (Mg), and Sodium (Na).
              </Card.Text>
              <Card.Text>
                These advanced parameters typically require specialized equipment and expertise. By predicting these parameters, we provide detailed insights into water quality, helping users avoid potential issues due to contamination.
              </Card.Text>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default ServicePage;
