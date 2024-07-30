import React ,{useState}from 'react';
import { BrowserRouter as Router, Route, Routes, Link, Navigate } from 'react-router-dom';
import HomePage from './pages/HomePage';
import WaterQualityPage from './pages/WaterQualityPage';
import AboutPage from './pages/About';
import Visualize from './pages/Visualize';
import LoginRegisterPage from './pages/Login';
import PrivateRoute from './components/PrivateRoute';
import { useAuth, AuthProvider } from './AuthContext';
import image from "./pages/image.jpg"
import './App.css';
import ConsultationPage from './pages/Consult';
import '@fortawesome/fontawesome-free/css/all.min.css';
import Footer from './components/footer';
import ServicePage from './pages/Service';


function App() {

  const [isLoggedOut, setIsLoggedOut] = useState(false);

  const onLogout = () => {
    handleLogout();
    setIsLoggedOut(true);

    // Remove the text after some time (e.g., 3 seconds)
    setTimeout(() => {
      setIsLoggedOut(false);
    }, 3500);
  };
  const { user, handleLogout } = useAuth();

  return (
    
      <Router>
        <div className="App">
          <nav className="navbar">
            <ul className="navbar-list">
              <li className="navbar-item">
                <Link to="/" className="navbar-link">
                

                <img src={image} alt="Logo" style={{ maxHeight: '100px', maxWidth: 'auto' }} />
                
                </Link>
              </li>
              <li className="navbar-item">
                <Link to="/about" className="navbar-link">About Us</Link>
              </li>
              <li className="navbar-item">
                <Link to="/services" className="navbar-link">Our Services</Link>
              </li>
              <li className="navbar-item">
                <Link to="/water-quality" className="navbar-link"> Predict Water Quality</Link>
              </li>
              
              <li className="navbar-item">
                <Link to="/visualize-data" className="navbar-link">Visualize Your Data</Link>
              </li>
              {user ? (
                <>
                  <li className="navbar-item">
                <span className="navbar-link">Welcome, Gurprem</span>
                
                  </li>
                  <li className="navbar-item">
                    <div className= "navbar-right">
                      
                  <a onClick={onLogout}
                       className="logout-button">
                     <i className="fas fa-sign-out-alt"></i> Logout</a>
                    </div>
                  </li>
                </>
              ) : (
                <li className="navbar-item">
                  <Link to="/login" className="navbar-link">Login</Link>
                </li>
            )}
            </ul>

          </nav>
           {isLoggedOut && (
        <div className='moving-text-container'>
          <div className='moving-text'>Successfully Logged Out</div>
        </div>
        
      )}

      
          <div className='content'>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/water-quality" element={<PrivateRoute><WaterQualityPage /></PrivateRoute>} />
              <Route path="/about" element={<AboutPage />} />
              <Route path="/services" element={<ServicePage />} />
              <Route path="/visualize-data" element={<PrivateRoute><Visualize /></PrivateRoute>} />
              <Route path="/login" element={user ? <Navigate to="/" /> : <LoginRegisterPage />} />
              <Route path="/consultation" element= {<ConsultationPage /> }/>
            </Routes>
          </div>
        </div>
      </Router>
    
  );
}
function AppWithAuthProvider() {
  return (
    <AuthProvider> {/* Wrap your App with AuthProvider */}
      <App />
      <Footer/>
    </AuthProvider>
  );
}
export default AppWithAuthProvider;
