import React from 'react';
import { useLocation } from 'react-router-dom';
import IconButton from '../components/tooltip';

const ConsultationPage = () => {
  const location = useLocation();
  
  const { input, predictions, WAWQI,} = location.state || {};
   // Add default empty object to avoid undefined error

   if (input) {
    delete input.selectedDate; // Remove 'selectedDate' key from input object
    delete input.selectedState; // Remove 'selectedDate' key from input object
  }

  if (!input || !predictions || !WAWQI ) {
    return <div>No data available</div>;
  }
  
   // Function to determine WQI range and return corresponding Bootstrap class
  const getWQIRangeClass = (wqi) => {
    if (wqi >= 0 && wqi <= 25) {
      return 'bg-success text-light';
    } else if (wqi > 25 && wqi <= 50) {
      return 'bg-info text-light';
    } else if (wqi > 50 && wqi <= 75) {
      return 'bg-warning text-dark';
    } else if (wqi > 75) {
      return 'bg-danger text-light';
    } else {
      return 'bg-secondary text-light'; // Default class if WQI is out of expected range
    }
  };


  // Function to classify parameter based on value and ranges
  const classifyParameter = (value, goodRange, normalRange) => {
    if (value >= goodRange[0] && value <= goodRange[1]) {
      return 'Good';
    } else if (value > normalRange[0] && value <= normalRange[1]) {
      return 'Normal';
    } else {
      return 'Bad';
    }
  };

  const keyToNameMapping = {
  ec: "Electrical Conductivity",
  ph: "pH",
  selectedDate: "Date",
  selectedState: "State",
  tds: "Total Dissolved Solids",
  temperature: "Temperature"
};

const predictionsKeyToNameMapping = {
  CO3: "Carbonate (CO3)",
  Ca: "Calcium (Ca)",
  Cl: "Chloride (Cl)",
  Mg: "Magnesium (Mg)",
  Na: "Sodium (Na)",
  SO4: "Sulfate (SO4)",
  TH: "Total Hardness (TH)"
};

  // Define ranges for each parameter
  const ranges = {
   ph: { good: [6.5, 8.0], normal: [8.1, 8.5] }, // Example ranges for pH
    ec: { good: [0, 700], normal: [701, 1500] }, // Example ranges for EC
    tds: { good: [0, 500], normal: [501, 1000] }, // Example ranges for TDS
    temperature: { good: [10, 24], normal: [25, 30] }, // Example ranges for Temperature
    CO3: { good: [0, 10], normal: [11, 30] }, // Example ranges for CO3
    Ca: { good: [0, 75], normal: [76, 100] }, // Example ranges for Ca
    Cl: { good: [0, 100], normal: [101, 250] }, // Example ranges for Cl
    Mg: { good: [0, 15], normal: [16, 40] }, // Example ranges for Mg
    Na: { good: [0, 10], normal: [11, 20] }, // Example ranges for Na
    SO4: { good: [0, 100], normal: [101, 250] }, // Example ranges for SO4
    TH: { good: [0, 60], normal: [61, 110] }, // Example ranges for TH

  };


   // Helper function to render classification badge
  const renderClassificationBadge = (value, key) => {
    const classification = classifyParameter(value, ranges[key].good, ranges[key].normal);
    let badgeClass = '';
    let text = '';

    switch (classification) {
      case 'Good':
        badgeClass = 'badge bg-success';
        text = 'Good';
        break;
      case 'Normal':
        badgeClass = 'badge bg-warning text-dark';
        text = 'Normal';
        break;
      case 'Bad':
        badgeClass = 'badge bg-danger';
        text = 'Bad';
        break;
      default:
        badgeClass = 'badge bg-secondary';
        text = 'Unknown';
    }

    return <span className={`mr-2 ${badgeClass}`}>{text}</span>;
  };

  // Define tooltips for each key
  const predictionTooltips = {
    CO3: 'Carbonates in drinking water affect pH levels. To control CO3 levels, use filtration systems or chemical treatments like pH adjustment to maintain a neutral pH level suitable for drinking.',
    Ca: 'Calcium is beneficial in moderate amounts but excessive levels can cause hardness. Use water softeners to reduce calcium hardness or reverse osmosis systems for precise control, ensuring optimal calcium levels for health benefits without water hardness.',
    Cl: 'Chloride levels are critical for taste and disinfection. Regular monitoring and treatment with activated carbon filtration or reverse osmosis can control chloride levels to meet regulatory standards for safe drinking water.',
    Mg: ' Magnesium contributes to water hardness and can affect taste. Use water softeners or ion exchange systems to regulate magnesium levels, ensuring water quality that meets taste preferences and health standards.',
    Na: 'Sodium levels in drinking water should be regulated, especially for individuals on low-sodium diets. Use reverse osmosis or distillation to reduce sodium content, ensuring safe drinking water for those with dietary restrictions.',
    SO4: 'Sulfates can affect taste and cause laxative effects at high levels. Treatment options include reverse osmosis or distillation to lower sulfate levels, ensuring safe and palatable drinking water.',
    TH: 'Total hardness is a measure of calcium and magnesium ions. Control hardness with water softeners or ion exchange systems to prevent scale buildup in pipes and appliances, ensuring water quality and plumbing longevity.'
    // Add tooltips for other keys as needed
  };

  const inputTooltips = {
    ec: 'Electrical conductivity indicates dissolved salts in water. Monitor EC levels regularly using conductivity meters. Use reverse osmosis or deionization systems to control EC, ensuring water is free from harmful salts and suitable for drinking.',
    ph: 'pH levels affect water taste and chemical reactions. Maintain pH within the range of 6.5 to 8.5 using pH meters and adjust with neutralization or acid/base treatments as necessary. Ensure pH stability for optimal drinking water quality.',
    temperature: 'Water temperature affects microbial growth and taste. Monitor and regulate water temperature to maintain it below 20°C for drinking purposes. Use temperature control devices or insulation to prevent microbial growth and ensure refreshing drinking water.',
    tds: 'TDS measures all inorganic and organic substances dissolved in water. Monitor TDS levels using TDS meters and treat with reverse osmosis or distillation to reduce TDS, ensuring water clarity and purity for safe consumption.'   
  }
   return (
    <div className="app-container" style={{color:'black'}}>
      <h1 className="mb-4">Consultation</h1>
      <h2 style={{padding: "30px"}}>For Household Usage</h2>

      <div className="card mb-4">
        <div className="card-header">
          <h2>Water Quality Index</h2>
          <div className={`p-3 text-center ${getWQIRangeClass(WAWQI)}`}>
            <h3 style={{textShadow: '1px 1px 2px rgba(0, 0, 0, 0.5)'}}>WQI: {WAWQI}</h3>
            <p className='mb-10' style={{ color: 'white', textShadow: '1px 1px 2px rgba(0, 0, 0, 0.5)', fontSize:'30px' }}>
              {WAWQI >= 0 && WAWQI <= 25 && 'Excellent'}
              {WAWQI > 25 && WAWQI <= 50 && 'Good'}
              {WAWQI > 50 && WAWQI <= 75 && 'Average'}
              {WAWQI > 75 && WAWQI <= 100 && 'Poor'}
              { WAWQI >= 100 && 'Very Poor'}

            </p>
          </div>
        </div>
      </div>

     <div className="row justify-content-center">
      <h2 style={{padding:'50px'}}>Predicted Parameters</h2>
        {/* Display each parameter */}
        {Object.keys(predictions).map((key) => (
          <div key={key} className="col-lg-4 mb-4">
            <div className="card hover-highlight">  
              <div className="card-header">
                <div style={{padding:"20px"}}>
                <IconButton keyName={key} tooltips={predictionTooltips} />
                </div>
                <h2>{predictionsKeyToNameMapping[key] || key}</h2>
              </div>
              <div className="card-body">
                <p className="mb-4"><strong>Value:</strong> {predictions[key]} (mg/L)</p>
                <p className="mb-2">
                  <strong>Result:</strong> {renderClassificationBadge(predictions[key], key)}
                  
                </p>
                  <span className="text-muted">
                    Good ({ranges[key].good[0]}-{ranges[key].good[1]}) , Normal ({ranges[key].normal[0]}-{ranges[key].normal[1]}) 
                  </span>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="row justify-content-center">
        <h2 style={{padding:'50px'}}>Input Parameters</h2>
        {/* Display input parameters */}
        {Object.keys(input).map((key) => (
          <div key={key} className="col-lg-6 mb-4">
            <div className="card hover-highlight">
              <div className="card-header">
                <div style={{padding:"20px"}}>
                <IconButton keyName={key} tooltips={inputTooltips} />
                </div>
                <h2>{keyToNameMapping[key] || key}</h2>
              </div>
              <div className="card-body">
                <p className="mb-1"><strong>Value:</strong> {input[key]}{key==='ec'|| key ==="tds"?(" (mg/L)"):key==='temperature'?(" (°C)"):("")}</p>

                <p className="mb-0">
                  <strong>Classification:</strong> {renderClassificationBadge(input[key], key)}
          
                </p>
                  <span className="text-muted">
                    Good ({ranges[key].good[0]}-{ranges[key].good[1]}) , Normal ({ranges[key].normal[0]}-{ranges[key].normal[1]}) 
                  </span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ConsultationPage;

