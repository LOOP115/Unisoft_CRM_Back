import React from "react";

function Login() {
  return (
    <div className="container">
      <div className="heading">
        <h1>Log in</h1>
      </div>
      <div className="form">
        <form>
          <label>Email: </label>
          <input name="email" type="text"/>
          <br />
          <br />
          <label>Password: </label>
          <input name="password" type="text" />
          <br />
          <br />
        </form>

        <button className="btn4" type="submit">
          Login
        </button>
      </div>
    </div>
  );
}

export default Login;
