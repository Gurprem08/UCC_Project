import React from 'react';
import { Container, Row, Col,Card } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import '../App.css';  // Import the custom CSS
import NN from "../NN.jpg"



function AboutPage() {
  
  return (
    <div className="water" >
      <Container className="about-page py-5">
        <Row>
          <Col>
            <h1 className="text-center mb-4 animated-title" style={{color:'black'}}>About Aqua Insights</h1>
          </Col>
        </Row>
        <Row>
          <Col md={{ span: 40, offset: 0 }}>
            <div className="about-description text-center animated-text">
              <p>
                Welcome to Aqua Insights, where we strive to bring the most advanced water quality analysis and insights to your fingertips. Our mission is to provide comprehensive and accurate water quality data that helps you make informed decisions to ensure the safety and health of your water resources.
              </p>
              <p>
                Our team of experts leverages the latest in technology and scientific research to deliver cutting-edge solutions for water quality monitoring. Whether you're managing a municipal water supply, conducting environmental research, or ensuring the purity of your private water source, Aqua Insights is here to support you with reliable and actionable data.
              </p>
              <p>
                At Aqua Insights, we are committed to sustainability and innovation. We believe in using our expertise to promote environmental stewardship and public health. Our state-of-the-art analytical tools and comprehensive data reporting make it easy for you to understand and manage water quality effectively.
              </p>
              <p>
                Join us in our vision to create a world where everyone has access to clean and safe water. Together, we can make a difference, one drop at a time.
              </p>
            </div>



          </Col>
        </Row>
        <Row className="my-4">
          <Col>
            <h1 className="text-center vision-title" style={{color:'black'}}>Our Vision</h1>
          </Col>
        </Row>
        <Row>
          <Col md={{ span: 40, offset: 0 }}>
            <div className="video-container">
              <video className="video w-100 animated-video" controls>
                <source src={`${process.env.PUBLIC_URL}/pitch.mp4`} type="video/mp4" />
                Your browser does not support the video tag.
              </video>
            </div>
          </Col>
        </Row>
      </Container>
    
    </div>
  );
}

export default AboutPage;

