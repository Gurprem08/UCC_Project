import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Form } from 'react-bootstrap';



  

const WaterQualityForm = () => {
  const [ph, setPh] = useState(7.0);
  const [ec, setEc] = useState(0.0);
  const [tds, setTds] = useState(0.0);
  const [temperature, setTemperature] = useState(20.0);
  const [predictions, setPredictions] = useState(null);
  const [selectedDate, handleDateChange] = useState("");
  const [ManualInput, setManualInput] = useState(null);
  const [selectedState, setSelectedState] = useState("Maharashtra");
  const [input, setInput] = useState(null); // Declare input state
  const [WAWQI, setWAWQI] = useState(0);
  const [loading, setLoading] = useState(false);
  const [csvFile, setCsvFile] = useState(null);
  const [data, setData] = useState(null);
  const [isChecked, setIsChecked] = useState(false);
  
  const navigate = useNavigate(); 





  const handle_default_csv = async (event)=>{
    event.preventDefault();
    try {
      const response = await axios.get('http://localhost:5000/api/default_csv', {
        responseType: 'blob', // Important to get the data as a blob
      });

      // Create a link element to download the CSV file
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'default_csv.csv'); // Set the file name
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (error) {
      console.error('Error downloading the CSV file', error);
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (ManualInput) {if (ph < 0 || ph > 14) {
      alert('pH value must be between 0 and 14');
      return;
    }}

    if (ManualInput) {if (ec <= 0 || ec > 8000) {
      alert('EC value must be between 1 and 8000 µS/cm');
      return;
    }}

    if (ManualInput) {if (tds <= 0 || tds > 2000) {
      alert('TDS value must be between 1 and 2000 mg/L');
      return;
    }}

    if (ManualInput) {if (temperature < 0 || temperature > 40 ){
      alert('Temperature must be between 0°C and 40°C');
      return;
    }}

    if (ManualInput) {if (!selectedDate) {
      alert('Please select a date.');
      return;
    }}
    if (ManualInput) {if (!selectedState) {
      alert('Please select a state.');
      return;
    }}
    
   
    setLoading(true)
    try {
      if (ManualInput){
      const response = await axios.post('http://localhost:5000/api/predict', {
        ph,
        ec,
        tds,
        temperature,
        selectedState,
        selectedDate,
      });
      const input = response.data.received;
      const predictions = response.data.predictions;
      const WAWQI = response.data.WAWQI;
    
      setPredictions(predictions);
      setInput(input);
      setWAWQI(WAWQI);

     
      

    }
      else{
        const formData = new FormData();
        formData.append('file', csvFile)
       const response = await axios.post('http://localhost:5000/api/predict_with_csv', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        });
      setData(JSON.parse(response.data.data));

     
      
    }

    } catch (error) {
      console.error(error);
    } finally{
      setLoading(false)
    }
  };
  
   const Navi = () =>{
        navigate('/consultation', { state: { input, predictions, WAWQI} });
      }


    const Navi_data = () =>{

        navigate('/consultation', { state: {data} });
      }   
  const downloadCSV = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/CSV', {
        responseType: 'blob', // Important to get the data as a blob
      });

      // Create a link element to download the CSV file
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'water_quality_predictions.csv'); // Set the file name
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (error) {
      console.error('Error downloading the CSV file', error);
    }
  };


  const stateOptions = [
  'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat',
  'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Kerala', 'Madhya Pradesh', 'Maharashtra',
  'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu',
  'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal'
];

const keyToNameMapping = {
  ec: "Electrical Conductivity (µS/cm)",
  ph: "pH",
  selectedDate: "Date",
  selectedState: "State",
  tds: "Total Dissolved Solids (mg/L)",
  temperature: "Temperature (°C)"
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

return (
  <div className="app-container">
  
    {ManualInput === null ? (
      <>
        <h1 style={{ padding: "60px", color: "black" , fontSize: "40px", fontWeight:'bold' , animation: "fadeInDown 1s ease-in-out"}}>Enter your Water Quality Parameters</h1>
        <div className="selection">
          <button style={{animation: "fadeInDown 1s ease-in-out", marginBottom:'100px'}}onClick={() => setManualInput(true)}>Using manual inputs</button>
          <button style={{animation: "fadeInDown 1s ease-in-out"}}onClick={() => setManualInput(false)}>Uploading CSV</button>
        </div>
      </>
    ) : (
      <div>
        {loading ? (
          <div className="spinner" ></div>
        ) : (
          <div>
            <div style={{ padding: '60px' }}>
              <button type="button" className="btn btn-primary btn-lg" style={{marginRight:'650px'}} onClick={() => {
                setManualInput(null);
                setPredictions(null);
                setInput(null);
                setData(null);
                setWAWQI(0);
              }}>Back</button>
            </div>
            {ManualInput ? (<h2 style={{ color: "black", animation: "fadeInDown 1s ease-in-out" }}>Please Enter Water Quality Parameters</h2>) : (<h2 style={{ color: "black", animation: "fadeInDown 1s ease-in-out" }}>Please Upload the CSV file </h2>)}
            {!ManualInput ? (
              <div className="upload-section">
                <button className="download-button" onClick={handle_default_csv}>Download default CSV template file</button>
                <div>
                  <input type="file" accept=".csv" onChange={(e) => setCsvFile(e.target.files[0])} />
      <Form.Group controlId="consentCheckbox" className="mt-4 checkbox-container">
      <Form.Check
        type="checkbox"
      
       
        checked={isChecked}
        onChange={() => { setIsChecked(prevState => !prevState) }}
        style={{ color: "black" }}
      />
      <Form.Label style={{ color: "black" , marginBottom:"20px"}}>This data may be used for model training purposes.</Form.Label>
    </Form.Group>
                  {isChecked && <button onClick={handleSubmit} disabled={!csvFile} style={{animation: "fadeInDown 0.5s ease-in-out"}}>Upload and Submit CSV file</button>}
                </div>
              </div>
            ) : (
             <div className="form-section">
  <form onSubmit={handleSubmit} style={{ border: "5px solid black", padding: "20px" }}>
    <div style={{ marginBottom: "10px" }}>
      <label style={{ display: "block" }}>
        <span style={{ color: "black", marginRight: "10px",fontSize: "25px", fontWeight:'bold'}}>pH Value:</span>
        <input
          type="number"
          value={ph}
          onChange={(event) => setPh(event.target.value)}
          style={{ width: "100px" }}
        />
      </label>
      <label style={{ display: "block" }}>
        <span style={{ color: "black", marginRight: "10px" ,fontSize: "25px", fontWeight:'bold' }}>Electrical Conductivity (µS/cm):</span>
        <input
          type="number"
          value={ec}
          onChange={(event) => setEc(event.target.value)}
          style={{ width: "100px" }}
        />
      </label>
    </div>
    <div style={{ marginBottom: "10px" }}>
      <label style={{ display: "block" }}>
        <span style={{ color: "black", marginRight: "10px", fontSize: "25px", fontWeight:'bold' }}>Total Dissolved Solids (mg/L):</span>
        <input
          type="number"
          value={tds}
          onChange={(event) => setTds(event.target.value)}
          style={{ width: "100px" }}
        />
      </label>
      <label style={{ display: "block" }}>
        <span style={{ color: "black", marginRight: "10px", fontSize: "25px", fontWeight:'bold' }}>Temperature (°C):</span>
        <input
          type="number"
          value={temperature}
          onChange={(event) => setTemperature(event.target.value)}
          style={{ width: "100px" }}
        />
      </label>
    </div>
    <div style={{ marginBottom: "10px" }}>
      <label style={{ display: "block" }}>
        <span style={{ color: "black", marginRight: "10px" , fontSize: "25px", fontWeight:'bold'}}>Select Your State:</span>
        <select
          value={selectedState}
          onChange={(event) => setSelectedState(event.target.value)}
          style={{ width: "150px" }}
        >
          <option value=""></option>
          {stateOptions.map((state) => (
            <option key={state} value={state}>{state}</option>
          ))}
        </select>
      </label>
      <label style={{ display: "block" }}>
        <span style={{ color: "black", marginRight: "10px", fontSize: "25px", fontWeight:'bold' }}>Select a date:</span>
        <input
          type="date"
          id="datepicker"
          name="datepicker"
          value={selectedDate}
          placeholder={new Date()}
          onChange={(event) => handleDateChange(event.target.value)}
          style={{ width: "150px" }}
        />
      </label>
    </div>
    <div style={{ marginBottom: "10px" }}>
      <Form.Group controlId="consentCheckbox" className="mt-4 checkbox-container">
      <Form.Check
        type="checkbox"
      
       
        checked={isChecked}
        onChange={() => { setIsChecked(prevState => !prevState) }}
        style={{ color: "black" }}
      />
      <Form.Label style={{ color: "black" , marginBottom:"20px"}}> This data will be used for model training purposes.</Form.Label>
    </Form.Group>
    </div>
    {isChecked && <button style={{animation: "fadeInDown 0.5s ease-in-out"}} type="submit" >Submit</button>}
  </form>
</div>

            )}
          </div>
        )}
      </div>
    )}

    {/* DATA COMING FROM MANUAL ENTRY */}
    <div className="container mt-5">
      {predictions && WAWQI >= 0 ? (
        <div>
          <div className='wqi-container'>
            <p className='animated-texting'>Water Quality Index: {WAWQI}</p>
          </div>
        </div>
      ) : predictions ? (
        <div>
          <div className='wqi-container'>
            <p className='animated-texting'>Water Quality Index: 0</p>
          </div>
        </div>
      ) : null}

      {predictions && (
        <div>
           
          <h2 style={{ color: "black" }}>Predicted Parameters</h2>
          <div className="table-responsive">
            <table className="styled-table ">
              <thead>
                <tr className='text-center'>
                  <th>Parameter</th>
                  <th>Value</th>
                </tr>
              </thead>
              <tbody className="table table-hover" style={{color:"black"}}>
                {Object.keys(predictions).map((key) => (
                  <tr key={key}>
                    <td>{predictionsKeyToNameMapping[key] || key} (mg/L)</td>
                    <td>{predictions[key]}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {input && (
        <div>
          <h2 style={{ color: "black" }}>Input Parameters</h2>
          <div className="table-container">
            <table className="styled-table">
              <thead>
                <tr className='text-center'>
                  <th>Parameter</th>
                  <th>Value</th>
                </tr>
              </thead>
              <tbody style={{color:"black"}}>
                {Object.keys(input).map((key) => (
                  <tr key={key}>
                    <td>{keyToNameMapping[key] || key || predictionsKeyToNameMapping[key]}</td>
                    <td>{input[key]}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div>
            <button className="download-button" onClick={downloadCSV}>Download CSV file</button>
            <button className="download-button" onClick={Navi}>
              Click for Consultation
            </button>
          </div>
        </div>
      )}

      {/* DATA COMING FROM CSV  */}
      {data && !WAWQI && !predictions && !input && (
        <div>
          <h2 style={{ color: "black" }}>Processed Data</h2>
          <div className="table-container">
            <table className="styled-table">
              <thead >
                <tr>
                  {Object.keys(data[0]).map((key) => (
                    <th key={key}>{key}</th>
                  ))}
                </tr>
              </thead>
              <tbody style={{color:"black"}}>
                {data.map((row, index) => (
                  <tr key={index}>
                    {Object.values(row).map((value, i) => (
                      <td key={i}>{value}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <button className="download-button" onClick={downloadCSV}>Download CSV file</button>
          <button className="download-button" onClick={Navi_data}>
            Click for Consultation
          </button>
        </div>
      )}
    </div>
  </div>
);

  
};

export default WaterQualityForm;