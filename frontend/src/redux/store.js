import { configureStore, getDefaultMiddleware } from "@reduxjs/toolkit";
import logger from 'redux-logger';

// Reducers
import { accountReducer } from "./slices/account"

let middleware = [...getDefaultMiddleware()]

if (process.env.REACT_APP_STAGE === "Dev") {
    middleware = [...middleware, logger]
}

export default configureStore({
    reducer: {
        account: accountReducer, 
    },
    middleware: middleware
})