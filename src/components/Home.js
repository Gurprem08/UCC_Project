import React from 'react';
import { Link,useLocation } from 'react-router-dom';
import { Card, Container, Row, Col, Carousel } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import '../App.css';  // Create a Home.css file for additional styling


import image1 from '../boy2.jpg';
import image2 from '../handpump.jpg';
import image3 from '../groundwater.jpg';
import gw from '../gwi.jpg'

const Home = () => {

  const cardData = [
    {
      title: 'Water Quality Matters',
      text: 'Water quality is essential for the health of humans, animals, and plants. Poor water quality can lead to diseases and environmental degradation.'
    },
    {
      title: 'Health Impact',
      text: 'Millions of people suffer from waterborne diseases every year. Ensuring clean water can significantly reduce health issues and save lives.'
    },
    {
      title: 'Environmental Impact',
      text: 'Polluted water affects ecosystems, harms wildlife, and disrupts natural processes. Protecting water quality is crucial for maintaining biodiversity.'
    },
    {
      title: 'Economic Impact',
      text: 'Poor water quality can lead to economic losses in sectors such as agriculture, fisheries, and tourism. Investing in water quality improvements can boost the economy.'
    },
    {
      title: 'Community Efforts',
      text: 'Communities around the world are taking action to improve water quality through education, conservation, and technology.'
    },
    {
      title: 'Our Mission',
      text: 'We are dedicated to monitoring water quality and providing actionable data to help ensure safe and clean water for everyone.'
    },
  ];

  return (
    <>
      <div className="main-container" style={{ backgroundColor: 'lightblue', animation: "fadeInDown 1s ease-in-out" }}>
        <div className="hero-section">
          <Link to="/water-quality">
            <button className='selection futuristic-button'>Click to analyze Your Water Quality</button>
          </Link>
        </div>

        <div className="content-section">
          <h1 className="title">Water Quality and Its Importance</h1>
          <Card className="h-100 hover-card" style={{margin:"100px"}}>
            <Card.Body>
              Water quality refers to the suitability of water for different uses according to its physical, chemical, biological, and organoleptic (taste-related) properties. High-quality and pure water is essential for daily use, agriculture, and industry; hence, understanding water quality is the first and crucial step to planning in the area of water purification and quality management.
              WHO reports that 785 million people lack basic drinking water and over 2 billion consume contaminated water, leading to diseases like cholera, diarrhoea, and typhoid. Annually, unsafe water causes 829,000 deaths, including 297,000 children under five.
              It is crucial to assess and predict water quality early on. This proactive approach provides a detailed understanding of the water before use, helping to prevent adverse effects from unrecognized contamination.
            </Card.Body>
          </Card>

          {/* Image Carousel */}
          <Carousel className="my-4">
            <Carousel.Item>
              <img className="d-block w-100" src= {image1} alt="First slide" />
            </Carousel.Item>

            <Carousel.Item>
              <img className="d-block w-100" src= {image2} alt="Second slide" />
    
              </Carousel.Item>
           
            <Carousel.Item>
              <img className="d-block w-100" src={image3} alt="Third slide" />
              </Carousel.Item>
  
          </Carousel>

         

          <h1 className="title" style={{marginTop:'100px'}}>Why Groundwater Is Important?</h1>
          <Card  style={{margin:"100px"}} >
            <Card.Img src={gw}/>
            <Card.Body>
              <h2 style={{}}>
                <li>
                Groundwater is a vital water supply for humanity.
                </li>
                <li>
                  It is a source of drinking water for 50% of the global population.
                </li>
                <li>
                  It accounts for 43% of all water used for irrigation.
                </li>
                <li>
Globally, approximately 2.5 billion individuals rely exclusively on groundwater resources to meet their fundamental daily water requirements.
                </li>
                <li>
Groundwater also plays a crucial role in sustaining healthy water ecosystems by supplying flow to wetlands and rivers.
                </li>
                
                </h2>
                

              
            </Card.Body>
          </Card>
        </div>

        <Container fluid className="pt-4">
          <h1 className="text-center mb-4" style={{ padding: "50px", color: 'black', fontWeight: "bold", marginbottom:'50px'}}>Why is Water Quality Awareness Important?</h1>
          <Row>
            {cardData.map((card, index) => (
              <Col key={index} md={4} className="mb-4">
                <Card className="h-100 hover-card">
                  <Card.Body>
                    <Card.Title>{card.title}</Card.Title>
                    <Card.Text>{card.text}</Card.Text>
                  </Card.Body>
                </Card>
              </Col>
            ))}
          </Row>
        </Container>
      </div>

    </>
  )
};

export default Home;


