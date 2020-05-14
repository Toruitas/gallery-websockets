import React, { useState, useCallback, useMemo, useEffect, useRef } from 'react';
import useWebSocket, { ReadyState } from 'react-use-websocket';
import { v4 as uuidv4 } from 'uuid';
import PointerImg from "./mouse.png"


// https://github.com/robtaussig/react-use-websocket

const wssProtocol = (window.location.protocol == 'https:') ? 'wss://': 'ws://';
const socketURL1 = wssProtocol + window.location.host + '/ws/gallery/';

export const GalleryWebSockets = () => {
    const [socketUrl, setSocketUrl] = useState(socketURL1);
    const [numUsers, setNumUsers] = useState(0);
    const [cursors, setCursors] = useState([]);
    const [lastUpdate, setLastUpdate] = useState();
    const [uuid, setUuid] = useState(uuidv4());

    const {
        sendMessage,
        sendJsonMessage,
        lastMessage,
        lastJsonMessage,
        readyState,
        getWebSocket
        } = useWebSocket(socketUrl, {
            onOpen: () => console.log('opened'),
            //Will attempt to reconnect on all close events, such as server shutting down
            shouldReconnect: (closeEvent) => true,
        });

    const connectionStatus = {
        [ReadyState.CONNECTING]: 'Connecting',
        [ReadyState.OPEN]: 'Open',
        [ReadyState.CLOSING]: 'Closing',
        [ReadyState.CLOSED]: 'Closed',
        [ReadyState.UNINSTANTIATED]: 'Uninstantiated',
      }[readyState];

    window.getWebSocket = getWebSocket;


    // messageHistory.current = useMemo(() => messageHistory.current.concat(lastMessage), [lastMessage]);

    const handleMoveSendPos = useCallback(
        ({ clientX, clientY }) => {
            sendJsonMessage({uuid:uuid, x: clientX, y: clientY })
        },
        []
    );

    // https://usehooks.com/useEventListener/
    useEventListener('mousemove', handleMoveSendPos);

    useEffect(()=>{
        if (lastJsonMessage){
            setNumUsers(Object.keys(lastJsonMessage).length-1);
            delete lastJsonMessage[uuid];  // remove own uuid
            let renderList = [];
            for (const [key, values] of Object.entries(lastJsonMessage)){
                let styling = {transform:`translate(${values["x"]}px, ${values["y"]}px)`};
                renderList.push(<img key={uuid} src={PointerImg} style={styling} />);
            }
            setCursors(renderList);
            console.log(cursors);
        }
    }, [lastJsonMessage]);

    return(
        <>
            <h1>this website displays other people's cursors</h1>
            <span>The WebSocket is currently {connectionStatus}</span>
            <p id="notice">there are {numUsers} other users on this website</p>
            {cursors}
        </>
    )

}


function useEventListener(eventName, handler, element = window){
    // https://usehooks.com/useEventListener/

    // Create a ref that stores handler
    const savedHandler = useRef();

    // Update ref.current value if handler changes.
    // This allows our effect below to always get latest handler ...
    // ... without us needing to pass it in effect deps array ...
    // ... and potentially cause effect to re-run every render.
    useEffect(() => {
      savedHandler.current = handler;
    }, [handler]);
  
    useEffect(
      () => {
        // Make sure element supports addEventListener
        // On 
        const isSupported = element && element.addEventListener;
  
        if (!isSupported) return;

        // Create event listener that calls handler function stored in ref
        const eventListener = event => savedHandler.current(event);
  
        // Add event listener
        element.addEventListener(eventName, eventListener);

        // Remove event listener on cleanup
        return () => {
          element.removeEventListener(eventName, eventListener);
        };
      },
      [eventName, element] // Re-run if eventName or element changes
    );
  };