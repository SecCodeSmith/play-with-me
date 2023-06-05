import "./left.css"
import "./icon.css"
import Icon from '@mui/material/Icon';
import VideogameAssetIcon from '@mui/icons-material/VideogameAsset';
import EventAvailableIcon from '@mui/icons-material/EventAvailable';
import EventIcon from '@mui/icons-material/Event';

export default function Left(){
    return(
        <div className="sidebar">
        <div className="sidebarWrapper">
          <ul className="sidebarList">
            <li className="sidebarListItem">
            <VideogameAssetIcon className="sidebarIcon"/>
              <span className="sidebarListItemText">Events</span>
            </li>
            <li className="sidebarListItem">
            <EventAvailableIcon className="sidebarIcon"/>
              <span className="sidebarListItemText">Dostępne eventy</span>
            </li>
            <li className="sidebarListItem">
            <EventIcon className="sidebarIcon"/>
              <span className="sidebarListItemText">Twoje eventy</span>
            </li>
            <li className="sidebarListItem">
            <EventIcon className="sidebarIcon"/>
              <span className="sidebarListItemText">Lista gier</span>
            </li>
            <li className="sidebarListItem">
            <EventIcon className="sidebarIcon"/>
              <span className="sidebarListItemText">Stwórz</span>
            </li>
            <li className="sidebarListItem">
            <EventIcon className="sidebarIcon"/>
              <span className="sidebarListItemText">Questions</span>
            </li>
            <li className="sidebarListItem">
            <EventIcon className="sidebarIcon"/>
              <span className="sidebarListItemText">Jobs</span>
            </li>
            <li className="sidebarListItem">
            <EventIcon className="sidebarIcon"/>
              <span className="sidebarListItemText">Events</span>
            </li>
            <li className="sidebarListItem">
            <EventIcon className="sidebarIcon"/>
              <span className="sidebarListItemText">Courses</span>
            </li>
          </ul>
          
            
          
        </div>
      </div>
        
    )
        
}