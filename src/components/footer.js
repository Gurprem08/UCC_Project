import React from 'react';
import logo from '../pages/image.jpg'

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-section">
          <h3 style={{fontFamily:'monospace', fontSize:'20px', marginLeft:'90px'}}>About Us</h3>
          <p style={{fontFamily:'monospace', fontSize:'20px'}}>Aqua Insights is a leading provider of advanced water quality monitoring and analysis solutions.</p>
        </div>
        {/* <div className='footer-section'>
          <img src={logo} alt="Logo" style={{ maxHeight: '100px', maxWidth: '500px', marginRight:'100px' }} />

        </div> */}
        <div className="footer-section">
          <h3 style={{fontFamily:'monospace', fontSize:'20px', marginLeft:'60px'}}>Contact Us</h3>
          <p style={{fontFamily:'monospace', fontSize:'20px'}}>Address: No-2, Cork Business Park, Cork Airport</p>
          <p style={{fontFamily:'monospace', fontSize:'20px'}}>Email: support@aqua.com<br />Phone: +353 845279125</p>
        </div>
      </div>
      <div className="footer-bottom">
        <p style={{fontWeight:'bold'}}>&copy; 2024 Aqua Insights. All rights reserved.</p>
      </div>
    </footer>
  );
};

export default Footer;
