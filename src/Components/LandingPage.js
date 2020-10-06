import React from "react";
import AboutMe from "./AboutMe";

export default class LandingPage extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            firstName: "",
            lastName: "",
            age: 0,
            showProfile: false
        }
    }



    // componentDidMount() {}

    // componentDidUpdate(prevProps, prevState, snapshot) {}

    handleInputChange = (event) => {
        const target = event.target;
        const value = target.type === 'checkbox' ? target.checked : target.value;
        const name = target.name;


        this.setState({
            [name]: value
        });
    }

    handleSubmit = (event) =>  {
        alert('Saved details Successfully')
        event.preventDefault();
    }

    backToLandingPage = () => {
        console.log("Going back to Main page")
        this.setState({
            showProfile: false
        })
    }

    render() {
        console.log(this.state)
        return (
            <div className="container-fluid">

                {
                    this.state.showProfile &&
                    <AboutMe
                        fname={this.state.firstName}
                        lname={this.state.lastName}
                        a={this.state.age}
                        sp={this.state.showProfile}
                        backToLandingPage={this.backToLandingPage}
                    />
                }

                {
                    !this.state.showProfile &&
                        <div className="container-fluid">
                            <br/>
                            <h3>Enter your details here</h3>

                            <form onSubmit={this.handleSubmit}>
                                <div className="form-group">
                                    <label htmlFor="firstName">First Name</label>
                                    <input type="text"
                                           className="form-control"
                                           id="firstName"
                                           name="firstName"
                                           placeholder="Enter First Name"
                                           value={this.state.firstName}
                                           onChange={this.handleInputChange}
                                    />

                                </div>

                                <div className="form-group">
                                    <label htmlFor="lastName">Last Name</label>
                                    <input type="text"
                                           className="form-control"
                                           id="lastName"
                                           name="lastName"
                                           placeholder="Enter Last Name"
                                           value={this.state.lastName}
                                           onChange={this.handleInputChange}
                                    />
                                </div>

                                <div className="form-group">
                                    <label htmlFor="age">Age</label>
                                    <input type="number"
                                           className="form-control"
                                           id="age"
                                           name="age"
                                           placeholder="Enter your Age"
                                           value={this.state.age}
                                           onChange={this.handleInputChange}
                                    />
                                </div>

                                <button type="submit" className="btn btn-primary">Submit</button>
                            </form>


                            <br/><br/>

                            <h3>Check your profile here</h3>

                            <button className="btn btn-primary"
                                    onClick={() => {
                                        this.setState({
                                            showProfile: true
                                        })
                                    }}>
                                Profile
                            </button>
                        </div>
                }
            </div>
        )
    }
}
