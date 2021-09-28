import React, { useState } from "react";

function CreateArea(props) {
  const [note, setNote] = useState({
    event: "",
    cname: "",
    date: "",
    time: "",
    address: "",
    notes: ""
  });

  function handleChange(event) {
    const { name, value } = event.target;

    setNote((prevNote) => {
      return {
        ...prevNote,
        [name]: value
      };
    });
  }

  function submitNote(event) {
    props.onAdd(note);
    setNote({
      event: "",
      cname: "",
      date: "",
      time: "",
      address: "",
      notes: ""
    });
    event.preventDefault();
  }

  return (
    <div>
      <form>
        <label>Event:</label>
        <input name="event" onChange={handleChange} value={note.event} /> <br />
        <label>Client Name:</label>
        <input name="cname" onChange={handleChange} value={note.cname} />
        <br />
        <label>Event Date:</label>
        <input name="date" onChange={handleChange} value={note.date} />
        <br />
        <label>Event Time:</label>
        <input name="time" onChange={handleChange} value={note.time} />
        <br />
        <label>Event Address:</label>
        <input name="address" onChange={handleChange} value={note.address} />
        <br />
        <label>Event Notes:</label>
        <textarea
          name="notes"
          onChange={handleChange}
          value={note.notes}
          placeholder="Take a note..."
          rows="3"
        />{" "}
        <br />
        <button onClick={submitNote}>Add</button>
      </form>
      <br />
      <br /> <br /> <br />
    </div>
  );
}

export default CreateArea;
