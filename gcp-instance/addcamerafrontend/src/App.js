import React from 'react';
import logo from './logo.svg';
import './App.css';
import axios from 'axios';




class App extends React.Component{

  constructor(props) {
    super(props);
    // Don't call this.setState() here!
    this.state = { rows: [] };
    
  }

  handleSubmit(e) {
    e.preventDefault();
    const rtsp = document.getElementById('rtsp').value;
    const lip = document.getElementById('local-ip').value;
    const lport = document.getElementById('local-port').value;
    const tport = document.getElementById('tunnel-port').value;
    const sip = document.getElementById('server-ip').value;
    const sport = document.getElementById('server-port').value;

    
    axios({
      method: "POST",
      url: "http://34.82.142.213:5000/add_camera",
      data: {
        rtsp:rtsp.toString(),
        lip:lip.toString(),
        lport:lport.toString(),
        tport:tport.toString(),
        sip:sip.toString(),
        sport:sport.toString()

      }
    }).then((response) => {
      console.log(response)
      if (response.data === 'success') {
        alert("Message Sent.");
        this.resetForm()
        this.getData()
      } else {
        alert("Message failed to send.")
      }
    })
  }
  componentDidMount(){
    this.getData()
  }

  getData(){
    axios({
      method: "GET",
      url: "http://34.82.142.213:5000/show_camera",
      
    }).then((response) => {
      console.log(response.data)
      this.setState({rows:response.data})
      console.log("rows",this.state.rows)
    })

  }

  resetForm() {
    document.getElementById('contact-form').reset();
  }
  Delete(e){
    console.log("Delete",e)
    axios({
      method: "POST",
      url: "http://34.82.142.213:5000/delete_camera",
      data: {
        rtsp:e.toString()
      }
    }).then((response) => {
      console.log(response)
      if (response.data === 'success') {
        alert("Delete Successful!");
        this.getData()
      } else {
        alert("Delete failed")
      }
    })

  }

  render(){
    return (
      <div className="App" style={{textAlign:'center'}} align="center">
       <form id="contact-form" onSubmit={this.handleSubmit.bind(this)} method="POST" style={{display:'inline-block',marginRight:'auto',marginLeft:'auto',width:'227px',paddingTop:'20vh'}}>
       <label for="rtsp">RTSP Link : <input type="text" id="rtsp" name="rtsp" /></label>
       <br/>
       <label for="local-ip">Camera Local IP : <input type="text" id="local-ip" name="local-ip" /></label>
       <br/>
       <label for="local-port">Camera Local Port : <input type="text" id="local-port" name="local-port" /></label>
       <br/>
       <label for="tunnel-port">Tunnel Port : <input type="text" id="tunnel-port" name="tunnel-port" /></label>
       <br/>
       <label for="server-ip">Server IP : <input type="text" id="server-ip" name="server-ip" /></label>
       <br/>
       <label for="server-port">Server Port : <input type="text" id="server-port" name="server-port" /></label>
       <br/>
       <button type="submit" value="save" style={{marginTop:'50px',marginRight:'50px'}}>Save</button>
       <button type="button" value="cancel" onClick={this.resetForm}>Cancel</button>
  
       </form>
       <table style={{marginRight:'auto',marginLeft:'auto',paddingTop:'20vh',textAlign:'left'}}>
       <tr>
         <th>RTSP Link</th>
         <th></th>
       </tr>
      {this.state.rows.map((row,i) => (
        
        <tr key={i}>
        {console.log("sdasda",row)}
          <td id={row}>{row}</td>
          <td><button type="button" value="cancel" onClick={()=>this.Delete(row)}>Delete</button></td>
        </tr>
      ))}
      </table>
      </div>
    )
  }
  
}

export default App;
