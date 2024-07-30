import React, { useEffect, useRef,useState } from 'react';
import socketIOClient from 'socket.io-client';


const ENDPOINT = 'http://127.0.0.1:5000';  

const VisualizeDataPage = () => {

  const [dataUpdated, setDataUpdated] = useState(false);

  const vizContainerRef = useRef(null);
  const vizRef = useRef(null);
  const socket = socketIOClient(ENDPOINT);
  console.log(socket)

  useEffect(() => {
    const initViz = () => {   
      
      const vizUrl = 'https://eu-west-1a.online.tableau.com/t/smitsangoi24082df7cab6/views/aqua_8/Main'  ;
      const vizOptions = {
        width: '100%',
        height: '100%',
        hideTabs: true,
        toolbarPosition: 'top',

      };
      
      if (vizRef.current) {
        vizRef.current.dispose();
      }
      const vizContainer = vizContainerRef.current;
      vizRef.current = new window.tableau.Viz(vizContainer, vizUrl, vizOptions);


    
    


    };


    // Function to dynamically load the Tableau JavaScript API
    const loadTableauScript = () => {
      return new Promise((resolve, reject) => {
        if (window.tableau) {
          resolve();
        } else {
          const script = document.createElement('script');
          script.src = 'https://eu-west-1a.online.tableau.com/javascripts/api/tableau-2.min.js';
          script.onload = resolve;
          script.onerror = reject;
          document.body.appendChild(script);
        }
      });
    };

    // Load the Tableau script and then initialize the viz
    loadTableauScript().then(initViz).catch(error => {
      console.error('Error loading Tableau script:', error);
      

 
    });



    // Cleanup
    return () => {
      if (vizRef.current) {
        vizRef.current.dispose();
      }

            // Listen for 'Important_message' event from backend
    
    
      // socket.on('Important_message', (data) => {
      //   console.log('Message for meeee:', data.message);
      //   if (data.message === "secret"){
      //     setDataUpdated(true);
      //     console.log("set data true")

      //   }
      // });

      setDataUpdated(true)


    };
  }, []);

      // Function to refresh Tableau Viz with new data
  const refreshData = () => {
    if (vizRef.current) {
      console.log("Refreshing data...");
      vizRef.current.refreshDataAsync(); // Refresh Tableau Viz
    }
  };
  

  if (dataUpdated){
    setTimeout(() => {
      
      refreshData();
    }, 3000);
    setDataUpdated(false)
  }


  return (
    <div className="visualize-container">
      <div className="content-box" style={{animation: "fadeInDown 1s ease-in-out" }}>
        <div >
        <h1 className="title" style={{ margin: '50px', animation: "fadeInDown 1s ease-in-out" }}>Visualizing Your Data</h1>
        </div>
          
        <div ref={vizContainerRef} className="viz-container" style={{ top: '120px', left: '70px', width: '90%', height: '90%' }}></div>
      </div>
    </div>
  );
}

export default VisualizeDataPage;
