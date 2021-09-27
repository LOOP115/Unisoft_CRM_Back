import React from "react";

function Card(props) {
  function handleClick() {
    props.onDelete(props.id);
  }

  return (
    <div className="event-card">
      <div className="event-card-top">
        <span>
          You have an event "{props.event}" with {props.cname}
        </span>
      </div>
      <div className="event-details">
        <ul>
          <li>Date: {props.date}</li>
          <li>Time: {props.time}</li>
          <li>Address: {props.address}</li>
          <li>Additional notes: {props.notes}</li>
        </ul>
        <button className="btn3">Edit</button>
        {"   "}
        <button className="btn3" onClick={handleClick}>
          Delete
        </button>
      </div>
    </div>
  );
}

export default Card;
