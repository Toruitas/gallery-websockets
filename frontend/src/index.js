import React from 'react'
import {render} from 'react-dom'
import {BrowserRouter} from 'react-router-dom'
import App from './App';
// import store from './app/store';
// import { Provider } from 'react-redux';
import * as serviceWorker from './serviceWorker';

render((
    // <Provider store={store}>
        <BrowserRouter>
            <App  />
        </BrowserRouter>
    // </Provider>
), document.getElementById('root'));

serviceWorker.unregister();