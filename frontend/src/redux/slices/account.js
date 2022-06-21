import { createSlice } from "@reduxjs/toolkit";

const accountInitialState = {
    selectedAccount: null,
};

export const accountSlice = createSlice({
    name: "account",
    initialState: accountInitialState,
    reducers: {
        setSelectedAccount: (state, action) => {
            state.selectedAccount = action.payload
        },
        resetAccount: state => accountInitialState
    }

})


export const { setSelectedAccount } = accountSlice.actions
export const accountReducer = accountSlice.reducer

