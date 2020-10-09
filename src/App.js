import React, {Component} from "react";
import axios from "axios";
import "./App.css";
class App extends Component {
  constructor(props) {
    super();
    this.state = {
      Url: "https://kfc19k33sc.execute-api.us-west-1.amazonaws.com/dev",
      result: [],
      post: {
        business_uid: "",
        business_type: "",
        business_type2: ""
      }
    };
  }

  clear = () => {
    this.setState({
      result: [],
      post: {
        business_type: "",
        business_uid: "",
        business_type2: ""
      }
    });
  };
  sendGetSlash = e => {
    const get_url = this.state.Url + e.target.value;
    console.log(get_url);
    axios
      .get(get_url)
      .then(res => {
        console.log(res);
        this.setState({result: res.data.result});
      })
      .catch(err => {
        console.error(err);
      });
  };
  sendGetArg = e => {
    const get_url = this.state.Url + e.target.value;
    console.log(get_url);
    axios
      .get(get_url, {
        params: {
          business_uid: "200-000001"
        }
      })
      .then(res => {
        console.log(res);
        this.setState({result: res.data.result});
      })
      .catch(err => {
        console.error(err);
      });
  };
  handleChange = e => {
    e.persist();
    this.setState(prevState => ({
      post: {
        ...prevState.post,
        [e.target.name]: e.target.value
      }
    }));
  };
  sendPostParam = e => {
    const get_url = this.state.Url + e.target.value;
    console.log(get_url);
    axios
      .post(`${get_url}/${this.state.post.business_type}`)
      .then(res => {
        console.log(res);
        let arr = [{message: res.data.message}];
        this.setState({result: arr});
      })
      .catch(err => {
        console.error(err);
      });
  };
  sendPostArgs = e => {
    const get_url = this.state.Url + e.target.value;
    console.log(get_url);
    let x = {
      business_uid: this.state.post.business_uid,
      business_type: this.state.post.business_type2
    };
    console.log(x);
    axios
      .post(get_url, x)
      .then(res => {
        console.log(res);
        let arr = [{message: res.data.message}];
        this.setState({result: arr});
      })
      .catch(err => {
        console.error(err);
      });
  };
  render() {
    return (
      <div className='row' style={{margin: "10px"}}>
        <div className='col'>
          <div>
            <p style={{display: "inline-flex", padding: "20px"}}>
              Sending get request to /api/v2/businesses
            </p>
            <button
              name='button1'
              value='/api/v2/businesses'
              className='btn btn-primary'
              onClick={this.sendGetSlash}
            >
              GET ALL
            </button>
          </div>
          <div>
            <p style={{display: "inline-flex", padding: "20px"}}>
              Sending get request to api/v2/onebusiness/200-000001
            </p>
            <button
              name='button2'
              value='/api/v2/onebusiness/200-000001'
              className='btn btn-primary'
              onClick={this.sendGetSlash}
            >
              GET SLASH
            </button>
          </div>
          <div>
            <p style={{display: "inline-flex", padding: "20px"}}>
              Sending get request to /api/v2/onebusinessarg
            </p>
            <button
              name='button3'
              value='/api/v2/onebusinessarg'
              className='btn btn-primary'
              onClick={this.sendGetArg}
            >
              GET ARGUMENTS
            </button>
          </div>
          <div>
            <div className='card'>
              <p style={{padding: "20px"}}>
                Sending POST request to /api/v2/updatebusinessparam/"post with
                param"
              </p>
              <div>
                <input
                  type='text'
                  name='business_type'
                  value={this.state.post.business_type}
                  placeholder='business_type'
                  style={{marginRight: "10px"}}
                  onChange={this.handleChange}
                />
                <button
                  name='button4'
                  value='/api/v2/updatebusinessparam'
                  className='btn btn-primary'
                  onClick={this.sendPostParam}
                >
                  POST PARAM
                </button>
              </div>
            </div>
          </div>
          <div>
            <div className='card'>
              <p style={{padding: "20px"}}>
                Sending POST request to /api/v2/updatebusinessparam/"post with
                JSON"
              </p>
              <div>
                <input
                  type='text'
                  name='business_uid'
                  value={this.state.post.business_uid}
                  placeholder='business_uid'
                  style={{marginRight: "10px"}}
                  onChange={this.handleChange}
                />
                <input
                  type='text'
                  name='business_type2'
                  value={this.state.post.business_type2}
                  placeholder='business_type'
                  style={{marginRight: "10px"}}
                  onChange={this.handleChange}
                />
                <button
                  name='button4'
                  value='/api/v2/updatebusinessparamjson'
                  className='btn btn-primary'
                  onClick={this.sendPostArgs}
                >
                  POST JSON
                </button>
              </div>
            </div>
          </div>
          <div>
            <button className='btn btn-danger' onClick={this.clear}>
              CLEAR
            </button>
          </div>
        </div>
        <div className='col' style={{backgroundColor: "#00ccff"}}>
          {this.state.result.map((val, id) => (
            <ul key={id}>
              {Object.keys(val).map((key, ind) => (
                <li>
                  {key}: {val[key]}
                </li>
              ))}
            </ul>
          ))}
        </div>
      </div>
    );
  }
}

export default App;
