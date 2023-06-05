import Topbar from "./Topbar";
import './home.css'
import Left from "./Left";
import Feed from "./Feed";
import Empty from "./Empty"

export default function Home(){
    return(
       <>
        <div>
            <div class="topbar-container">
                
            <Topbar/>
            </div>
        
        
        

                <div className="homeContainer">
                <Left/>
                <Feed/>
                <Empty/>
                </div>
            </div>
        </>
        
    );
}