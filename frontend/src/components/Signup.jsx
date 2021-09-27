import React from "react";

function Signup() {
  return (
    <div className="container">
      <div className="heading">
        <h1>Sign up</h1>
      </div>
      <div className="form">
        <form>
          <label>Name: </label>
          <input name="name" type="text"/>
          <br />
          <br />
          <label>Email: </label>
          <input name="email" type="text"/>

          <br />
          <br />
          <label>Password: </label>
          <input name="password" type="text" />
          <br />
          <br />
          <label>Re-input Password: </label>
          <input name="password" type="text"/>
          <br />
          <br />
        </form>

        <button className="btn4" type="submit">
          Signup
        </button>
      </div>
    </div>
  );
}

export default Signup;
