import React from "react";

export default class AboutMe extends React.Component {

    constructor(props) {
        super(props);
    }

    state = {

    }

    // componentDidMount() {}

    // componentDidUpdate(prevProps, prevState, snapshot) {}

    render() {
        return (
            <div className="container-fluid">

                <h3>Your Profile</h3>

                <p>I am {this.props.fname} {this.props.lname}. I'm {this.props.a} years old</p>

                <button className="btn btn-primary"
                        onClick={() => {
                           this.props.backToLandingPage();
                        }}>
                    Home
                </button>

            </div>
        )
    }

}
