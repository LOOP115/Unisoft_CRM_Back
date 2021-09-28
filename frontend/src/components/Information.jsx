import React from "react";

function Info(){
    const textStyle = {
        textAlign:"center",
    }

    return(
        <div className="home-content">
        <h2 style = {textStyle}>We provide</h2>
        <table className="home-content-detail">
            <td>
                <div className = "home-content-detail-text">
                    <tr><h3>Store Your Contacts</h3></tr>
                    <tr>Paper Free, Indexing in lightning speed</tr>
                </div>
                <tr><img className = "home-content-img" src = "https://media.istockphoto.com/photos/aerial-view-of-crowd-connected-by-lines-picture-id1180187740?b=1&k=20&m=1180187740&s=170667a&w=0&h=QOfnYYbuOvnEV-XgM0QNP_Rk1mFyNVuxgOkLIUwI-YQ=" alt = "contact_img" /></tr>
            </td>
            <td>
                <div className = "home-content-detail-text">
                    <tr><h3>Key Dates Reminder</h3></tr>
                    <tr>So that you wont't forget anything</tr>
                </div>
                <tr><img className = "home-content-img" src = "https://media.istockphoto.com/photos/close-up-of-calendar-on-the-table-planning-for-business-meeting-or-picture-id995353918?b=1&k=20&m=995353918&s=170667a&w=0&h=mEfKniHJfu9-zc9ijrFFcGygm8OFdAW40wuwNni8FWo=" alt = "contact_img" /></tr>
            </td>
            <td>
                <div className = "home-content-detail-text">
                    <tr ><h3>Auto Templated Email</h3></tr>
                    <tr>Easier life with automated stuff</tr>
                </div>
                <tr><img className = "home-content-img" src = "https://media.istockphoto.com/photos/email-marketing-concept-picture-id1282799241?b=1&k=20&m=1282799241&s=170667a&w=0&h=0MRaTWVvtApyUjK2I4wOMbQSDD0HMSxP-I_O7egPFDQ=" alt = "contact_img" /></tr>
            </td>
        </table>
        </div>
    );

}

export default Info;