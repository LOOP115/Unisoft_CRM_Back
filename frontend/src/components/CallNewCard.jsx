import React, { useState } from "react";
import Footer from "./Footer";
import Card from "./Card";
import CreateArea from "./CreateArea";

function CallNewCard() {
  const [notes, setNotes] = useState([]);

  function addNote(newNote) {
    setNotes((prevNotes) => {
      return [...prevNotes, newNote];
    });
  }

  function deleteNote(id) {
    setNotes((prevNotes) => {
      return prevNotes.filter((noteItem, index) => {
        return index !== id;
      });
    });
  }

  return (
    <div>
      <header>
        <h1>Activities</h1>
      </header>
      <CreateArea onAdd={addNote} />
      {notes.map((noteItem, index) => {
        return (
          <Card
            key={index}
            id={index}
            event={noteItem.event}
            cname={noteItem.cname}
            date={noteItem.date}
            time={noteItem.time}
            address={noteItem.address}
            notes={noteItem.notes}
            onDelete={deleteNote}
          />
        );
      })}
      <Footer />
    </div>
  );
}

export default CallNewCard;
