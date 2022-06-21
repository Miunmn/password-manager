// Libraries
// import React, { useContext } from "react";
import {   Navigate  } from "react-router-dom";
import { useSelector } from "react-redux";

// Context
// import { UserContext } from "./UserContext";

const PrivateRoute = (props) => {
    const { component: Component, path, componentProps, ...rest } = props;
    
    const user_id = useSelector(state => state.account.selectedAccount);
    const loading = false;
    // const { user_id, loading} = useContext(UserContext);
    // let history = useNavigate();

    if (!user_id && !loading) return <Navigate
        to={{
            pathname: "/",
        }}
    />
    // if (isUserAllowed) return <Component {...props} {...componentProps} />
    // return <NotAuthorized />
    return <Component {...props} {...componentProps} />


};

export default PrivateRoute;
