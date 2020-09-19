import React, {useState} from "react";
import axios from "axios";
import "./App.css";
function App() {
  const Url = "https://kfc19k33sc.execute-api.us-west-1.amazonaws.com/dev";
  const [result, setResult] = useState([]);
  const [post, setPost] = useState({business_uid: "", business_type: ""});
  const clear = () => {
    setResult([]);
  };
  const sendGetSlash = e => {
    const get_url = Url + e.target.value;
    console.log(get_url);
    axios
      .get(get_url)
      .then(res => {
        console.log(res);
        setResult(res.data.result);
      })
      .catch(err => {
        console.error(err);
      });
  };
  const sendGetArg = e => {
    const get_url = Url + e.target.value;
    console.log(get_url);
    axios
      .get(get_url, {
        params: {
          business_uid: "200-000001"
        }
      })
      .then(res => {
        console.log(res);
        setResult(res.data.result);
      })
      .catch(err => {
        console.error(err);
      });
  };
  const handleChange = e => {
    e.persist();
    setPost({...post, [e.target.name]: e.target.value});
    console.log(post);
  };
  const sendPostParam = e => {
    const get_url = Url + e.target.value;
    console.log(get_url);
    axios
      .post(`${get_url}/${post.business_type}`)
      .then(res => {
        console.log(res);
        let arr = [{message: res.data.message}];
        setResult(arr);
      })
      .catch(err => {
        console.error(err);
      });
  };
  const sendPostArgs = e => {
    const get_url = Url + e.target.value;
    console.log(get_url);
    axios
      .post(get_url, {
        business_uid: post.business_uid,
        business_type: post.business_type
      })
      .then(res => {
        console.log(res);
        let arr = [{message: res.data.message}];
        setResult(arr);
      })
      .catch(err => {
        console.error(err);
      });
  };
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
            onClick={sendGetSlash}
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
            onClick={sendGetSlash}
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
            onClick={sendGetArg}
          >
            GET ARGUMENTS
          </button>
        </div>
        <div>
          <div className='card'>
            <p style={{padding: "20px"}}>
              Sending POST request to /api/v2/updatebusinessparam/Meal
              Subscription
            </p>
            <div>
              <input
                type='text'
                name='business_type'
                placeholder='post with param'
                style={{marginRight: "10px"}}
                onChange={handleChange}
              />
              <button
                name='button4'
                value='/api/v2/updatebusinessparam'
                className='btn btn-primary'
                onClick={sendPostParam}
              >
                POST PARAM
              </button>
            </div>
          </div>
        </div>
        <div>
          <div className='card'>
            <p style={{padding: "20px"}}>
              Sending POST request to /api/v2/updatebusinessparam/Meal
              Subscription
            </p>
            <div>
              <input
                type='text'
                name='business_uid'
                placeholder='business_uid'
                style={{marginRight: "10px"}}
                onChange={handleChange}
              />
              <input
                type='text'
                name='business_type'
                placeholder='business_type'
                style={{marginRight: "10px"}}
                onChange={handleChange}
              />
              <button
                name='button4'
                value='/api/v2/updatebusinessparam'
                className='btn btn-primary'
                onClick={sendPostParam}
              >
                POST PARAM
              </button>
            </div>
          </div>
        </div>
        <div>
          <button className='btn btn-danger' onClick={clear}>
            CLEAR
          </button>
        </div>
      </div>
      <div className='col' style={{backgroundColor: "#00ccff"}}>
        {result.map((val, id) => (
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

export default App;
