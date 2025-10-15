

// import React, { useEffect, useRef, useState, useCallback } from "react";
// import Hls from "hls.js";
// import { Rnd } from "react-rnd";

// const API_BASE = "/api";

// // --- Helper Hooks & Functions ---

// const useDebouncedCallback = (callback, delay) => {
//   const timeoutRef = useRef(null);
//   useEffect(() => () => clearTimeout(timeoutRef.current), []);
//   return (...args) => {
//     clearTimeout(timeoutRef.current);
//     timeoutRef.current = setTimeout(() => {
//       callback(...args);
//     }, delay);
//   };
// };

// const percent = (num, denom) => (denom <= 0 ? 0 : (num / denom) * 100);
// const clamp = (v, min, max) => Math.max(min, Math.min(max, v));


// // --- Styles ---

// const styles = {
//   page: { 
//     minHeight: "100vh", 
//     background: "#0f1419",
//     fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
//   },
//   container: { 
//     maxWidth: "100%", 
//     margin: "0 auto", 
//     padding: "20px 24px" 
//   },
//   header: { 
//     display: "flex", 
//     alignItems: "center", 
//     gap: 16, 
//     marginBottom: 24,
//     flexWrap: "wrap" 
//   },
//   title: { 
//     color: "#fff", 
//     fontSize: 24, 
//     fontWeight: 700,
//     letterSpacing: "-0.5px"
//   },
//   input: {
//     flex: 1, 
//     minWidth: 300, 
//     padding: "12px 16px", 
//     borderRadius: 10, 
//     border: "1px solid #2d3548",
//     background: "#161b2e", 
//     color: "#e8ecf7", 
//     outline: "none",
//     fontSize: 14,
//     transition: "border-color 0.2s, background 0.2s",
//   },
//   button: (variant = "primary", disabled = false) => ({
//     padding: "12px 20px",
//     borderRadius: 10,
//     border: "none",
//     background: variant === "primary" 
//       ? (disabled ? "#2a3a5a" : "linear-gradient(135deg, #4c6fff 0%, #3b5bdb 100%)")
//       : (disabled ? "#1a2030" : "#1e2538"),
//     color: disabled ? "#5a6380" : "#fff",
//     cursor: disabled ? "not-allowed" : "pointer",
//     fontWeight: 600,
//     fontSize: 14,
//     transition: "transform 0.1s, box-shadow 0.2s, background-color 0.2s",
//     boxShadow: variant === "primary" && !disabled ? "0 4px 12px rgba(76, 111, 255, 0.3)" : "none",
//     display: "flex",
//     alignItems: "center",
//     justifyContent: "center",
//     gap: 8,
//   }),
//   layout: { 
//     display: "grid", 
//     gridTemplateColumns: "280px 1fr 300px", 
//     gap: 20,
//     alignItems: "start"
//   },
//   panel: { 
//     background: "rgba(22, 27, 46, 0.9)", 
//     border: "1px solid #2d3548", 
//     borderRadius: 16, 
//     padding: 20,
//     color: "#e8ecf7",
//     backdropFilter: "blur(10px)"
//   },
//   panelTitle: { 
//     fontWeight: 700, 
//     fontSize: 16, 
//     marginBottom: 16, 
//     color: "#fff",
//     letterSpacing: "-0.3px"
//   },
//   playerWrap: {
//     position: "relative", 
//     borderRadius: 16, 
//     overflow: "hidden",
//     border: "1px solid #2d3548", 
//     background: "#000",
//     boxShadow: "0 8px 32px rgba(0, 0, 0, 0.4)"
//   },
//   playerBox: { 
//     position: "relative", 
//     width: "100%", 
//     aspectRatio: "16/9",
//     background: "#000",
//     backgroundImage: "linear-gradient(rgba(255,255,255,0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.05) 1px, transparent 1px)",
//     backgroundSize: "20px 20px",
//   },
//   video: { 
//     width: "100%", 
//     height: "100%", 
//     display: "block" 
//   },
//   overlayCanvas: { 
//     position: "absolute", 
//     inset: 0, 
//     pointerEvents: "none" 
//   },
//   overlayItem: (isSelected) => ({ 
//     pointerEvents: "auto", 
//     border: isSelected ? "2px solid #4c6fff" : "1px dashed rgba(255, 255, 255, 0.4)",
//     boxShadow: isSelected ? "0 0 0 3px rgba(76, 111, 255, 0.2)" : "none",
//     borderRadius: 8, 
//     overflow: "hidden", 
//     display: "flex", 
//     alignItems: "center", 
//     justifyContent: "center", 
//     color: "#fff", 
//     background: "transparent",
//     transition: "border-color 0.2s, box-shadow 0.2s"
//   }),
//   propRow: { 
//     display: "grid", 
//     gridTemplateColumns: "80px 1fr",
//     alignItems: "center", 
//     gap: 10, 
//     marginBottom: 12 
//   },
//   propLabel: {
//     fontSize: 13,
//     fontWeight: 600,
//     color: "#a0aec0"
//   },
//   smallInput: { 
//     width: "100%",
//     padding: "8px 12px", 
//     borderRadius: 8, 
//     border: "1px solid #2d3548", 
//     background: "#0f1423", 
//     color: "#e8ecf7", 
//     outline: "none",
//     fontSize: 13
//   },
//   listItem: (isSelected) => ({ 
//     display: "flex", 
//     alignItems: "center", 
//     justifyContent: "space-between", 
//     gap: 10, 
//     padding: "10px 12px", 
//     borderRadius: 10, 
//     background: isSelected ? "#1a2442" : "#0f1423",
//     border: "1px solid",
//     borderColor: isSelected ? "#4c6fff" : "#252b3f",
//     cursor: "pointer",
//     transition: "all 0.2s"
//   }),
//   chip: (isLive) => ({
//     padding: "8px 16px", 
//     borderRadius: 999, 
//     background: isLive 
//       ? "linear-gradient(135deg, #10b981 0%, #059669 100%)"
//       : "#374151",
//     color: isLive ? "#fff" : "#9ca3af",
//     boxShadow: isLive ? "0 4px 12px rgba(16, 185, 129, 0.3)" : "none",
//     fontWeight: 700, 
//     fontSize: 12,
//     letterSpacing: "0.5px"
//   }),
//   ghostBtn: { 
//     background: "#1e2538", 
//     border: "1px solid #2d3548", 
//     color: "#e8ecf7", 
//     padding: "8px 12px", 
//     borderRadius: 8, 
//     cursor: "pointer",
//     fontSize: 13,
//     fontWeight: 600,
//     transition: "all 0.2s"
//   },
//   errorMsg: {
//     padding: "12px 16px",
//     borderRadius: 10,
//     background: "rgba(239, 68, 68, 0.1)",
//     border: "1px solid rgba(239, 68, 68, 0.3)",
//     color: "#fca5a5",
//     marginBottom: 16,
//     fontSize: 14
//   }
// };

// // --- App Component ---

// export default function App() {
//   const videoRef = useRef(null);
//   const containerRef = useRef(null);
//   const hlsRef = useRef(null);

//   const [rtspUrl, setRtspUrl] = useState("");
//   const [hlsUrl, setHlsUrl] = useState("");
//   const [streamId, setStreamId] = useState("");
//   const [isLive, setIsLive] = useState(false);
//   const [loading, setLoading] = useState(false);
//   const [overlays, setOverlays] = useState([]);
//   const [selectedId, setSelectedId] = useState(null);
//   const [snapGrid, setSnapGrid] = useState(false);
//   const [error, setError] = useState("");

//   const selected = overlays.find(o => o._id === selectedId) || null;

//   // HLS.js video setup
//   useEffect(() => {
//     if (!hlsUrl || !videoRef.current) return;
//     const video = videoRef.current;

//     if (Hls.isSupported()) {
//       const hls = new Hls({ liveDurationInfinity: true, lowLatencyMode: true });
//       hls.loadSource(hlsUrl);
//       hls.attachMedia(video);
//       hls.on(Hls.Events.MANIFEST_PARSED, () => setIsLive(true));
//       hls.on(Hls.Events.ERROR, (_, data) => {
//         if (data?.fatal) {
//           setError("Stream error, please retry");
//           setIsLive(false);
//         }
//       });
//       hlsRef.current = hls;
//       return () => {
//         hls.destroy();
//         hlsRef.current = null;
//       };
//     } else if (video.canPlayType("application/vnd.apple.mpegurl")) {
//       video.src = hlsUrl;
//     }
//   }, [hlsUrl]);

//   // Stream controls
//   const startStream = async () => {
//     setError("");
//     setLoading(true);
//     try {
//       const res = await fetch(`${API_BASE}/stream/start`, {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ rtsp_url: rtspUrl }),
//       });
//       const data = await res.json();
//       if (data.success) {
//         setHlsUrl(data.hls_url);
//         setStreamId(data.stream_id);
//       } else {
//         setError(data.error || "Failed to start stream");
//       }
//     } catch (e) {
//       setError("Failed to start stream");
//     } finally {
//       setLoading(false);
//     }
//   };

//   const stopStream = async () => {
//     try {
//       await fetch(`${API_BASE}/stream/stop`, {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ stream_id: streamId }),
//       });
//     } catch {}
//     if (hlsRef.current) {
//       hlsRef.current.destroy();
//       hlsRef.current = null;
//     }
//     setIsLive(false);
//     setStreamId("");
//     setHlsUrl("");
//   };

//   // Overlay API calls
//   const fetchOverlays = useCallback(async () => {
//     try {
//       const res = await fetch(`${API_BASE}/overlays`);
//       const data = await res.json();
//       setOverlays(Array.isArray(data) ? data : []);
//     } catch {}
//   }, []);

//   useEffect(() => {
//     fetchOverlays();
//   }, [fetchOverlays]);

//   const createOverlay = async (payload) => {
//     const res = await fetch(`${API_BASE}/overlays`, {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify(payload),
//     });
//     const newOverlay = await res.json();
//     await fetchOverlays();
//     if (newOverlay?._id) setSelectedId(newOverlay._id);
//   };

//   const updateOverlayAPI = async (id, patch) => {
//     await fetch(`${API_BASE}/overlays/${id}`, {
//       method: "PUT",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify(patch),
//     });
//     await fetchOverlays();
//   };
  
//   const debouncedUpdateOverlay = useDebouncedCallback(updateOverlayAPI, 400);

//   const updateOverlay = (id, patch) => {
//     // Update local state immediately for responsiveness
//     setOverlays(prev => prev.map(o => o._id === id ? { ...o, ...patch } : o));
//     // Debounce the API call
//     debouncedUpdateOverlay(id, patch);
//   };

//   const deleteOverlay = async (id) => {
//     await fetch(`${API_BASE}/overlays/${id}`, { method: "DELETE" });
//     if (id === selectedId) setSelectedId(null);
//     await fetchOverlays();
//   };

//   // Coordinate conversion
//   const toPercentBox = (x, y, w, h) => {
//     const rect = containerRef.current?.getBoundingClientRect();
//     if (!rect) return { xPercent: 0, yPercent: 0, widthPercent: 20, heightPercent: 10 };
//     return {
//       xPercent: clamp(percent(x, rect.width), 0, 100),
//       yPercent: clamp(percent(y, rect.height), 0, 100),
//       widthPercent: clamp(percent(w, rect.width), 2, 100),
//       heightPercent: clamp(percent(h, rect.height), 2, 100),
//     };
//   };

//   const toPxBox = (ov) => {
//     const rect = containerRef.current?.getBoundingClientRect();
//     const w = rect?.width || 1, h = rect?.height || 1;
//     return {
//       x: (ov.xPercent / 100) * w,
//       y: (ov.yPercent / 100) * h,
//       width: (ov.widthPercent / 100) * w,
//       height: (ov.heightPercent / 100) * h,
//     };
//   };

//   // Keyboard shortcuts - FIXED
//   useEffect(() => {
//     const onKey = (e) => {
//       // **FIX:** Check if the event originated from an input or textarea.
//       // If it did, don't trigger global shortcuts.
//       const targetNode = e.target.tagName.toUpperCase();
//       if (targetNode === 'INPUT' || targetNode === 'TEXTAREA') {
//         return;
//       }
      
//       if (!selected) return;

//       const step = e.shiftKey ? 3 : 1;
//       const dx = e.key === "ArrowRight" ? step : e.key === "ArrowLeft" ? -step : 0;
//       const dy = e.key === "ArrowDown" ? step : e.key === "ArrowUp" ? -step : 0;
      
//       if (dx || dy) {
//         e.preventDefault();
//         updateOverlay(selected._id, {
//           xPercent: clamp((selected.xPercent || 0) + dx, 0, 100),
//           yPercent: clamp((selected.yPercent || 0) + dy, 0, 100),
//         });
//       }

//       if (e.key === "Delete" || e.key === "Backspace") {
//         e.preventDefault();
//         deleteOverlay(selected._id);
//       }
//     };
//     window.addEventListener("keydown", onKey);
//     return () => window.removeEventListener("keydown", onKey);
//   }, [selected, overlays]); // Re-bind if selected overlay data changes

//   // Overlay creation actions
//   const addText = () => {
//     createOverlay({
//       name: "Text Overlay", type: "text", content: "Sample Text",
//       xPercent: 5, yPercent: 5, widthPercent: 25, heightPercent: 10, zIndex: 5, visible: true,
//     });
//   };

//   const addLogo = () => {
//     createOverlay({
//       name: "Logo", type: "image", content: "https://via.placeholder.com/150",
//       xPercent: 75, yPercent: 6, widthPercent: 18, heightPercent: 14, zIndex: 10, visible: true,
//     });
//   };

//   const useSample = () => setRtspUrl("rtsp://localhost:8554/live");

//   return (
//     <div style={styles.page}>
//       <div style={styles.container}>
//         {/* Header */}
//         <div style={styles.header}>
//           <div style={styles.title}>🎥 Live RTSP Player</div>
//           <span style={{ flex: 1 }} />
//           <div style={styles.chip(isLive)}>
//             {isLive ? "● LIVE" : "○ IDLE"}
//           </div>
//         </div>

//         {/* Stream Controls */}
//         <div style={styles.header}>
//           <input
//             style={styles.input}
//             placeholder="Enter RTSP URL (rtsp://...)"
//             value={rtspUrl}
//             onChange={(e) => setRtspUrl(e.target.value)}
//           />
//           <button style={styles.button("secondary")} onClick={useSample}>Use Sample</button>
//           <button style={styles.button("primary", loading || !rtspUrl)} onClick={startStream} disabled={loading || !rtspUrl}>
//             {loading ? "Starting..." : "Start Stream"}
//           </button>
//           <button style={styles.button("secondary", !streamId)} onClick={stopStream} disabled={!streamId}>
//             Stop Stream
//           </button>
//         </div>
        
//         {error && <div style={styles.errorMsg}>⚠️ {error}</div>}

//         {/* Main Layout */}
//         <div style={styles.layout}>
          
//           {/* Left Panel: Overlay Manager */}
//           <div style={styles.panel}>
//             <div style={styles.panelTitle}>Overlay Manager</div>
//             <div style={{ display: "flex", gap: 8, marginBottom: 16 }}>
//               <button style={{...styles.ghostBtn, flex: 1}} onClick={addText}>+ Text</button>
//               <button style={{...styles.ghostBtn, flex: 1}} onClick={addLogo}>+ Logo</button>
//             </div>
//             <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 16, padding: "8px 12px", background: "#0f1423", borderRadius: 8 }}>
//               <label style={{ display: "flex", alignItems: "center", gap: 8, cursor: "pointer", fontSize: 13, width: '100%' }}>
//                 <input type="checkbox" checked={snapGrid} onChange={(e) => setSnapGrid(e.target.checked)} />
//                 Grid Overlay
//               </label>
//             </div>
//             <div style={{ display: "grid", gap: 8, maxHeight: 400, overflowY: "auto" }}>
//               {overlays.length === 0 ? (
//                 <div style={{ opacity: 0.5, textAlign: "center", padding: 20, fontSize: 13 }}>
//                   No overlays yet.
//                 </div>
//               ) : (
//                 overlays
//                   .sort((a, b) => (b.zIndex || 0) - (a.zIndex || 0))
//                   .map((o) => (
//                     <div key={o._id} style={styles.listItem(selectedId === o._id)} onClick={() => setSelectedId(o._id)}>
//                       <div style={{ display: "flex", gap: 10, alignItems: "center", flex: 1, minWidth: 0 }}>
//                         <span style={{fontSize: 16}}>{o.type === 'text' ? '✏️' : '🖼️'}</span>
//                         <div style={{ fontWeight: 600, fontSize: 13, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
//                           {o.name}
//                         </div>
//                       </div>
//                       <button
//                         title={o.visible ? "Hide" : "Show"}
//                         style={{...styles.ghostBtn, padding: "4px 8px", fontSize: 11, background: 'transparent'}}
//                         onClick={(e) => {
//                           e.stopPropagation();
//                           updateOverlay(o._id, { visible: !o.visible });
//                         }}
//                       >
//                         {o.visible ? "👁️" : "🙈"}
//                       </button>
//                     </div>
//                   ))
//               )}
//             </div>
//           </div>

//           {/* Center Panel: Video Player */}
//           <div style={styles.playerWrap}>
//             <div ref={containerRef} style={styles.playerBox}>
//               <video ref={videoRef} controls style={styles.video} playsInline autoPlay muted />
//               <div style={styles.overlayCanvas}>
//                 {snapGrid && <div style={{position: "absolute", inset: 0, backgroundImage: "linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px)", backgroundSize: "5% 5%", pointerEvents: "none"}} />}
//                 {overlays.filter(o => o.visible).map((o) => {
//                   const px = toPxBox(o);
//                   return (
//                     <Rnd
//                       key={o._id}
//                       size={{ width: px.width, height: px.height }}
//                       position={{ x: px.x, y: px.y }}
//                       bounds="parent"
//                       onDragStop={(_, data) => {
//                         const patch = toPercentBox(data.x, data.y, data.node.offsetWidth, data.node.offsetHeight);
//                         updateOverlayAPI(o._id, { xPercent: patch.xPercent, yPercent: patch.yPercent });
//                       }}
//                       onResizeStop={(_, __, ref, ___, pos) => {
//                         const patch = toPercentBox(pos.x, pos.y, ref.offsetWidth, ref.offsetHeight);
//                         updateOverlayAPI(o._id, patch);
//                       }}
//                       onClick={() => setSelectedId(o._id)}
//                       enableResizing={{ top: true, right: true, bottom: true, left: true, topRight: true, bottomRight: true, bottomLeft: true, topLeft: true }}
//                       style={styles.overlayItem(selectedId === o._id)}
//                       dragGrid={snapGrid && containerRef.current ? [containerRef.current.clientWidth * 0.05, containerRef.current.clientHeight * 0.05] : [1,1]}
//                       resizeGrid={snapGrid && containerRef.current ? [containerRef.current.clientWidth * 0.05, containerRef.current.clientHeight * 0.05] : [1,1]}
//                     >
//                       {o.type === "text" ? (
//                         <div style={{ padding: 12, fontWeight: 700, textShadow: "0 2px 4px rgba(0,0,0,0.8)", whiteSpace: "pre-wrap", textAlign: "center", fontSize: 16 }}>
//                           {o.content}
//                         </div>
//                       ) : (
//                         <img src={o.content} alt={o.name} style={{ width: "100%", height: "100%", objectFit: "contain", pointerEvents: "none" }} />
//                       )}
//                     </Rnd>
//                   );
//                 })}
//               </div>
//             </div>
//           </div>

//           {/* Right Panel: Properties */}
//           <div style={styles.panel}>
//             <div style={styles.panelTitle}>Properties</div>
//             {!selected ? (
//               <div style={{ opacity: 0.5, textAlign: "center", padding: 32, fontSize: 13 }}>
//                 Select an overlay to edit properties.
//               </div>
//             ) : (
//               <div style={{ display: "grid", gap: 4 }}>
//                 <div style={styles.propRow}>
//                   <label style={styles.propLabel}>Name</label>
//                   <input style={styles.smallInput} value={selected.name || ""} onChange={(e) => updateOverlay(selected._id, { name: e.target.value })} />
//                 </div>
//                 <div style={styles.propRow}>
//                   <label style={styles.propLabel}>Type</label>
//                   <div style={{...styles.smallInput, background: '#0a0e1a', display: 'flex', alignItems: 'center'}}>{selected.type}</div>
//                 </div>
//                 <div style={styles.propRow}>
//                   <label style={styles.propLabel}>{selected.type === "text" ? "Text" : "URL"}</label>
//                   <input style={styles.smallInput} value={selected.content || ""} onChange={(e) => updateOverlay(selected._id, { content: e.target.value })} />
//                 </div>
//                 <div style={styles.propRow}>
//                   <label style={styles.propLabel}>Z-Index</label>
//                   <input type="number" style={styles.smallInput} value={selected.zIndex ?? 5} onChange={(e) => updateOverlay(selected._id, { zIndex: Number(e.target.value) })} />
//                 </div>
                
//                 {/* Position and Size Grid */}
//                 <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8, padding: "12px", background: "#0f1423", borderRadius: 8, marginTop: 8 }}>
//                   {[
//                     {label: 'X %', key: 'xPercent'}, {label: 'Y %', key: 'yPercent'},
//                     {label: 'Width %', key: 'widthPercent'}, {label: 'Height %', key: 'heightPercent'}
//                   ].map(item => (
//                     <div key={item.key}>
//                       <label style={{ fontSize: 12, color: "#9ca3af", marginBottom: 4, display: "block" }}>{item.label}</label>
//                       <input
//                         type="number"
//                         style={{...styles.smallInput, padding: '6px 10px'}}
//                         value={Math.round(selected[item.key] || 0)}
//                         onChange={(e) => updateOverlay(selected._id, { [item.key]: clamp(Number(e.target.value), 0, 100) })}
//                       />
//                     </div>
//                   ))}
//                 </div>

//                 {/* Action Buttons */}
//                 <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8, marginTop: 16 }}>
//                   <button style={styles.ghostBtn} onClick={() => updateOverlay(selected._id, { visible: !selected.visible })}>
//                     {selected.visible ? "Hide" : "Show"}
//                   </button>
//                   <button 
//                     style={{...styles.ghostBtn, borderColor: "rgba(239, 68, 68, 0.4)", color: "#fca5a5"}} 
//                     onClick={() => deleteOverlay(selected._id)}>
//                     Delete
//                   </button>
//                 </div>

//                 {/* Hint Box */}
//                 <div style={{ marginTop: 16, padding: "10px 12px", background: "#0f1423", borderRadius: 8, fontSize: 11, color: "#9ca3af", lineHeight: 1.5 }}>
//                   <strong>💡 Pro-Tip:</strong> Use arrow keys to nudge, hold Shift to move faster, and press Delete to remove the selected overlay.
//                 </div>
//               </div>
//             )}
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// }



import React, { useEffect, useRef, useState, useCallback } from "react";
import Hls from "hls.js";
import { Rnd } from "react-rnd";

const API_BASE = "/api";

// --- Helper Hooks & Functions ---

const useDebouncedCallback = (callback, delay) => {
  const timeoutRef = useRef(null);
  useEffect(() => () => clearTimeout(timeoutRef.current), []);
  return (...args) => {
    clearTimeout(timeoutRef.current);
    timeoutRef.current = setTimeout(() => {
      callback(...args);
    }, delay);
  };
};

const percent = (num, denom) => (denom <= 0 ? 0 : (num / denom) * 100);
const clamp = (v, min, max) => Math.max(min, Math.min(max, v));


// --- Styles ---

const styles = {
  page: { 
    minHeight: "100vh", 
    background: "#0f1419",
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
  },
  container: { 
    maxWidth: "100%", 
    margin: "0 auto", 
    padding: "20px 24px" 
  },
  header: { 
    display: "flex", 
    alignItems: "center", 
    gap: 16, 
    marginBottom: 24,
    flexWrap: "wrap" 
  },
  title: { 
    color: "#fff", 
    fontSize: 24, 
    fontWeight: 700,
    letterSpacing: "-0.5px"
  },
  input: {
    flex: 1, 
    minWidth: 300, 
    padding: "12px 16px", 
    borderRadius: 10, 
    border: "1px solid #2d3548",
    background: "#161b2e", 
    color: "#e8ecf7", 
    outline: "none",
    fontSize: 14,
    transition: "border-color 0.2s, background 0.2s",
  },
  button: (variant = "primary", disabled = false) => ({
    padding: "12px 20px",
    borderRadius: 10,
    border: "none",
    background: variant === "primary" 
      ? (disabled ? "#2a3a5a" : "linear-gradient(135deg, #4c6fff 0%, #3b5bdb 100%)")
      : (disabled ? "#1a2030" : "#1e2538"),
    color: disabled ? "#5a6380" : "#fff",
    cursor: disabled ? "not-allowed" : "pointer",
    fontWeight: 600,
    fontSize: 14,
    transition: "transform 0.1s, box-shadow 0.2s, background-color 0.2s",
    boxShadow: variant === "primary" && !disabled ? "0 4px 12px rgba(76, 111, 255, 0.3)" : "none",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    gap: 8,
  }),
  layout: { 
    display: "grid", 
    gridTemplateColumns: "280px 1fr 300px", 
    gap: 20,
    alignItems: "start"
  },
  panel: { 
    background: "rgba(22, 27, 46, 0.9)", 
    border: "1px solid #2d3548", 
    borderRadius: 16, 
    padding: 20,
    color: "#e8ecf7",
    backdropFilter: "blur(10px)"
  },
  panelTitle: { 
    fontWeight: 700, 
    fontSize: 16, 
    marginBottom: 16, 
    color: "#fff",
    letterSpacing: "-0.3px"
  },
  playerWrap: {
    position: "relative", 
    borderRadius: 16, 
    overflow: "hidden",
    border: "1px solid #2d3548", 
    background: "#000",
    boxShadow: "0 8px 32px rgba(0, 0, 0, 0.4)"
  },
  playerBox: { 
    position: "relative", 
    width: "100%", 
    aspectRatio: "16/9",
    background: "#000",
    backgroundImage: "linear-gradient(rgba(255,255,255,0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.05) 1px, transparent 1px)",
    backgroundSize: "20px 20px",
  },
  video: { 
    width: "100%", 
    height: "100%", 
    display: "block" 
  },
  overlayCanvas: { 
    position: "absolute", 
    inset: 0, 
    pointerEvents: "none" 
  },
  overlayItem: (isSelected) => ({ 
    pointerEvents: "auto", 
    border: isSelected ? "2px solid #4c6fff" : "1px dashed rgba(255, 255, 255, 0.4)",
    boxShadow: isSelected ? "0 0 0 3px rgba(76, 111, 255, 0.2)" : "none",
    borderRadius: 8, 
    overflow: "hidden", 
    display: "flex", 
    alignItems: "center", 
    justifyContent: "center", 
    color: "#fff", 
    background: "transparent",
    transition: "border-color 0.2s, box-shadow 0.2s"
  }),
  propRow: { 
    display: "grid", 
    gridTemplateColumns: "80px 1fr",
    alignItems: "center", 
    gap: 10, 
    marginBottom: 12 
  },
  propLabel: {
    fontSize: 13,
    fontWeight: 600,
    color: "#a0aec0"
  },
  smallInput: { 
    width: "100%",
    padding: "8px 12px", 
    borderRadius: 8, 
    border: "1px solid #2d3548", 
    background: "#0f1423", 
    color: "#e8ecf7", 
    outline: "none",
    fontSize: 13
  },
  listItem: (isSelected) => ({ 
    display: "flex", 
    alignItems: "center", 
    justifyContent: "space-between", 
    gap: 10, 
    padding: "10px 12px", 
    borderRadius: 10, 
    background: isSelected ? "#1a2442" : "#0f1423",
    border: "1px solid",
    borderColor: isSelected ? "#4c6fff" : "#252b3f",
    cursor: "pointer",
    transition: "all 0.2s"
  }),
  chip: (isLive) => ({
    padding: "8px 16px", 
    borderRadius: 999, 
    background: isLive 
      ? "linear-gradient(135deg, #10b981 0%, #059669 100%)"
      : "#374151",
    color: isLive ? "#fff" : "#9ca3af",
    boxShadow: isLive ? "0 4px 12px rgba(16, 185, 129, 0.3)" : "none",
    fontWeight: 700, 
    fontSize: 12,
    letterSpacing: "0.5px"
  }),
  ghostBtn: { 
    background: "#1e2538", 
    border: "1px solid #2d3548", 
    color: "#e8ecf7", 
    padding: "8px 12px", 
    borderRadius: 8, 
    cursor: "pointer",
    fontSize: 13,
    fontWeight: 600,
    transition: "all 0.2s"
  },
  errorMsg: {
    padding: "12px 16px",
    borderRadius: 10,
    background: "rgba(239, 68, 68, 0.1)",
    border: "1px solid rgba(239, 68, 68, 0.3)",
    color: "#fca5a5",
    marginBottom: 16,
    fontSize: 14
  }
};

// --- App Component ---

export default function App() {
  const videoRef = useRef(null);
  const containerRef = useRef(null);
  const hlsRef = useRef(null);

  const [rtspUrl, setRtspUrl] = useState("");
  const [hlsUrl, setHlsUrl] = useState("");
  const [streamId, setStreamId] = useState("");
  const [isLive, setIsLive] = useState(false);
  const [loading, setLoading] = useState(false);
  const [overlays, setOverlays] = useState([]);
  const [selectedId, setSelectedId] = useState(null);
  const [snapGrid, setSnapGrid] = useState(false);
  const [error, setError] = useState("");

  const selected = overlays.find(o => o._id === selectedId) || null;

  // HLS.js video setup
  useEffect(() => {
    if (!hlsUrl || !videoRef.current) return;
    const video = videoRef.current;

    if (Hls.isSupported()) {
      const hls = new Hls({ liveDurationInfinity: true, lowLatencyMode: true });
      hls.loadSource(hlsUrl);
      hls.attachMedia(video);
      hls.on(Hls.Events.MANIFEST_PARSED, () => setIsLive(true));
      hls.on(Hls.Events.ERROR, (_, data) => {
        if (data?.fatal) {
          setError("Stream error, please retry");
          setIsLive(false);
        }
      });
      hlsRef.current = hls;
      return () => {
        hls.destroy();
        hlsRef.current = null;
      };
    } else if (video.canPlayType("application/vnd.apple.mpegurl")) {
      video.src = hlsUrl;
    }
  }, [hlsUrl]);

  // Stream controls
  const startStream = async () => {
    setError("");
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/stream/start`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ rtsp_url: rtspUrl }),
      });
      const data = await res.json();
      if (data.success) {
        setHlsUrl(data.hls_url);
        setStreamId(data.stream_id);
      } else {
        setError(data.error || "Failed to start stream");
      }
    } catch (e) {
      setError("Failed to start stream");
    } finally {
      setLoading(false);
    }
  };

  const stopStream = async () => {
    try {
      await fetch(`${API_BASE}/stream/stop`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ stream_id: streamId }),
      });
    } catch {}
    if (hlsRef.current) {
      hlsRef.current.destroy();
      hlsRef.current = null;
    }
    setIsLive(false);
    setStreamId("");
    setHlsUrl("");
  };

  // Overlay API calls
  const fetchOverlays = useCallback(async () => {
    try {
      const res = await fetch(`${API_BASE}/overlays`);
      const data = await res.json();
      setOverlays(Array.isArray(data) ? data : []);
    } catch {}
  }, []);

  useEffect(() => {
    fetchOverlays();
  }, [fetchOverlays]);

  const createOverlay = async (payload) => {
    const res = await fetch(`${API_BASE}/overlays`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const newOverlay = await res.json();
    await fetchOverlays();
    if (newOverlay?._id) setSelectedId(newOverlay._id);
  };

  const updateOverlayAPI = async (id, patch) => {
    await fetch(`${API_BASE}/overlays/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(patch),
    });
    await fetchOverlays();
  };
  
  const debouncedUpdateOverlay = useDebouncedCallback(updateOverlayAPI, 400);

  const updateOverlay = (id, patch) => {
    // Update local state immediately for responsiveness
    setOverlays(prev => prev.map(o => o._id === id ? { ...o, ...patch } : o));
    // Debounce the API call
    debouncedUpdateOverlay(id, patch);
  };

  const deleteOverlay = async (id) => {
    await fetch(`${API_BASE}/overlays/${id}`, { method: "DELETE" });
    if (id === selectedId) setSelectedId(null);
    await fetchOverlays();
  };

  // Coordinate conversion
  const toPercentBox = (x, y, w, h) => {
    const rect = containerRef.current?.getBoundingClientRect();
    if (!rect) return { xPercent: 0, yPercent: 0, widthPercent: 20, heightPercent: 10 };
    return {
      xPercent: clamp(percent(x, rect.width), 0, 100),
      yPercent: clamp(percent(y, rect.height), 0, 100),
      widthPercent: clamp(percent(w, rect.width), 2, 100),
      heightPercent: clamp(percent(h, rect.height), 2, 100),
    };
  };

  const toPxBox = (ov) => {
    const rect = containerRef.current?.getBoundingClientRect();
    const w = rect?.width || 1, h = rect?.height || 1;
    return {
      x: (ov.xPercent / 100) * w,
      y: (ov.yPercent / 100) * h,
      width: (ov.widthPercent / 100) * w,
      height: (ov.heightPercent / 100) * h,
    };
  };

  // Keyboard shortcuts
  useEffect(() => {
    const onKey = (e) => {
      const targetNode = e.target.tagName.toUpperCase();
      if (targetNode === 'INPUT' || targetNode === 'TEXTAREA') {
        return;
      }
      
      if (!selected) return;

      const step = e.shiftKey ? 3 : 1;
      const dx = e.key === "ArrowRight" ? step : e.key === "ArrowLeft" ? -step : 0;
      const dy = e.key === "ArrowDown" ? step : e.key === "ArrowUp" ? -step : 0;
      
      if (dx || dy) {
        e.preventDefault();
        updateOverlay(selected._id, {
          xPercent: clamp((selected.xPercent || 0) + dx, 0, 100),
          yPercent: clamp((selected.yPercent || 0) + dy, 0, 100),
        });
      }

      if (e.key === "Delete" || e.key === "Backspace") {
        e.preventDefault();
        deleteOverlay(selected._id);
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [selected, overlays]); 

  // Overlay creation actions
  const addText = () => {
    createOverlay({
      name: "Text Overlay", type: "text", content: "Sample Text",
      xPercent: 5, yPercent: 5, widthPercent: 25, heightPercent: 10, zIndex: 5, visible: true,
    });
  };

  const addLogo = () => {
    createOverlay({
      name: "Logo", type: "image", content: "https://via.placeholder.com/150",
      xPercent: 75, yPercent: 6, widthPercent: 18, heightPercent: 14, zIndex: 10, visible: true,
    });
  };

  const useSample = () => setRtspUrl("rtsp://localhost:8554/live");

  return (
    <div style={styles.page}>
      <div style={styles.container}>
        {/* Header */}
        <div style={styles.header}>
          <div style={styles.title}>🎥 Live RTSP Player</div>
          <span style={{ flex: 1 }} />
          <div style={styles.chip(isLive)}>
            {isLive ? "● LIVE" : "○ IDLE"}
          </div>
        </div>

        {/* Stream Controls */}
        <div style={styles.header}>
          <input
            style={styles.input}
            placeholder="Enter RTSP URL (rtsp://...)"
            value={rtspUrl}
            onChange={(e) => setRtspUrl(e.target.value)}
          />
          <button style={styles.button("secondary")} onClick={useSample}>Use Sample</button>
          <button style={styles.button("primary", loading || !rtspUrl)} onClick={startStream} disabled={loading || !rtspUrl}>
            {loading ? "Starting..." : "Start Stream"}
          </button>
          <button style={styles.button("secondary", !streamId)} onClick={stopStream} disabled={!streamId}>
            Stop Stream
          </button>
        </div>
        
        {error && <div style={styles.errorMsg}>⚠️ {error}</div>}

        {/* Main Layout */}
        <div style={styles.layout}>
          
          {/* Left Panel: Overlay Manager */}
          <div style={styles.panel}>
            <div style={styles.panelTitle}>Overlay Manager</div>
            <div style={{ display: "flex", gap: 8, marginBottom: 16 }}>
              <button style={{...styles.ghostBtn, flex: 1}} onClick={addText}>+ Text</button>
              <button style={{...styles.ghostBtn, flex: 1}} onClick={addLogo}>+ Logo</button>
            </div>
            <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 16, padding: "8px 12px", background: "#0f1423", borderRadius: 8 }}>
              <label style={{ display: "flex", alignItems: "center", gap: 8, cursor: "pointer", fontSize: 13, width: '100%' }}>
                <input type="checkbox" checked={snapGrid} onChange={(e) => setSnapGrid(e.target.checked)} />
                Grid Overlay
              </label>
            </div>
            <div style={{ display: "grid", gap: 8, maxHeight: 400, overflowY: "auto" }}>
              {overlays.length === 0 ? (
                <div style={{ opacity: 0.5, textAlign: "center", padding: 20, fontSize: 13 }}>
                  No overlays yet.
                </div>
              ) : (
                overlays
                  .sort((a, b) => (b.zIndex || 0) - (a.zIndex || 0))
                  .map((o) => (
                    <div 
                      key={o._id} 
                      style={styles.listItem(selectedId === o._id)} 
                      // --- CHANGED: Toggling selection logic ---
                      onClick={() => setSelectedId(selectedId === o._id ? null : o._id)}
                    >
                      <div style={{ display: "flex", gap: 10, alignItems: "center", flex: 1, minWidth: 0 }}>
                        <span style={{fontSize: 16}}>{o.type === 'text' ? '✏️' : '🖼️'}</span>
                        <div style={{ fontWeight: 600, fontSize: 13, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                          {o.name}
                        </div>
                      </div>
                      <button
                        title={o.visible ? "Hide" : "Show"}
                        style={{...styles.ghostBtn, padding: "4px 8px", fontSize: 11, background: 'transparent'}}
                        onClick={(e) => {
                          e.stopPropagation();
                          updateOverlay(o._id, { visible: !o.visible });
                        }}
                      >
                        {o.visible ? "👁️" : "🙈"}
                      </button>
                    </div>
                  ))
              )}
            </div>
          </div>

          {/* Center Panel: Video Player */}
          <div style={styles.playerWrap}>
            <div 
              ref={containerRef} 
              style={styles.playerBox} 
              // --- ADDED: Unselect when clicking video background ---
              onClick={() => setSelectedId(null)}
            >
              <video ref={videoRef} controls style={styles.video} playsInline autoPlay muted />
              <div style={styles.overlayCanvas}>
                {snapGrid && <div style={{position: "absolute", inset: 0, backgroundImage: "linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px)", backgroundSize: "5% 5%", pointerEvents: "none"}} />}
                {overlays.filter(o => o.visible).map((o) => {
                  const px = toPxBox(o);
                  return (
                    <Rnd
                      key={o._id}
                      size={{ width: px.width, height: px.height }}
                      position={{ x: px.x, y: px.y }}
                      bounds="parent"
                      onDragStop={(_, data) => {
                        const patch = toPercentBox(data.x, data.y, data.node.offsetWidth, data.node.offsetHeight);
                        updateOverlayAPI(o._id, { xPercent: patch.xPercent, yPercent: patch.yPercent });
                      }}
                      onResizeStop={(_, __, ref, ___, pos) => {
                        const patch = toPercentBox(pos.x, pos.y, ref.offsetWidth, ref.offsetHeight);
                        updateOverlayAPI(o._id, patch);
                      }}
                      // --- CHANGED: Added event propagation stop and toggle logic ---
                      onClick={(e) => {
                        e.stopPropagation(); // Prevents the background click from firing
                        setSelectedId(selectedId === o._id ? null : o._id);
                      }}
                      enableResizing={{ top: true, right: true, bottom: true, left: true, topRight: true, bottomRight: true, bottomLeft: true, topLeft: true }}
                      style={styles.overlayItem(selectedId === o._id)}
                      dragGrid={snapGrid && containerRef.current ? [containerRef.current.clientWidth * 0.05, containerRef.current.clientHeight * 0.05] : [1,1]}
                      resizeGrid={snapGrid && containerRef.current ? [containerRef.current.clientWidth * 0.05, containerRef.current.clientHeight * 0.05] : [1,1]}
                    >
                      {o.type === "text" ? (
                        <div style={{ padding: 12, fontWeight: 700, textShadow: "0 2px 4px rgba(0,0,0,0.8)", whiteSpace: "pre-wrap", textAlign: "center", fontSize: 16 }}>
                          {o.content}
                        </div>
                      ) : (
                        <img src={o.content} alt={o.name} style={{ width: "100%", height: "100%", objectFit: "contain", pointerEvents: "none" }} />
                      )}
                    </Rnd>
                  );
                })}
              </div>
            </div>
          </div>

          {/* Right Panel: Properties */}
          <div style={styles.panel}>
            <div style={styles.panelTitle}>Properties</div>
            {!selected ? (
              <div style={{ opacity: 0.5, textAlign: "center", padding: 32, fontSize: 13 }}>
                Select an overlay to edit properties.
              </div>
            ) : (
              <div style={{ display: "grid", gap: 4 }}>
                <div style={styles.propRow}>
                  <label style={styles.propLabel}>Name</label>
                  <input style={styles.smallInput} value={selected.name || ""} onChange={(e) => updateOverlay(selected._id, { name: e.target.value })} />
                </div>
                <div style={styles.propRow}>
                  <label style={styles.propLabel}>Type</label>
                  <div style={{...styles.smallInput, background: '#0a0e1a', display: 'flex', alignItems: 'center'}}>{selected.type}</div>
                </div>
                <div style={styles.propRow}>
                  <label style={styles.propLabel}>{selected.type === "text" ? "Text" : "URL"}</label>
                  <input style={styles.smallInput} value={selected.content || ""} onChange={(e) => updateOverlay(selected._id, { content: e.target.value })} />
                </div>
                <div style={styles.propRow}>
                  <label style={styles.propLabel}>Z-Index</label>
                  <input type="number" style={styles.smallInput} value={selected.zIndex ?? 5} onChange={(e) => updateOverlay(selected._id, { zIndex: Number(e.target.value) })} />
                </div>
                
                {/* Position and Size Grid */}
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8, padding: "12px", background: "#0f1423", borderRadius: 8, marginTop: 8 }}>
                  {[
                    {label: 'X %', key: 'xPercent'}, {label: 'Y %', key: 'yPercent'},
                    {label: 'Width %', key: 'widthPercent'}, {label: 'Height %', key: 'heightPercent'}
                  ].map(item => (
                    <div key={item.key}>
                      <label style={{ fontSize: 12, color: "#9ca3af", marginBottom: 4, display: "block" }}>{item.label}</label>
                      <input
                        type="number"
                        style={{...styles.smallInput, padding: '6px 10px'}}
                        value={Math.round(selected[item.key] || 0)}
                        onChange={(e) => updateOverlay(selected._id, { [item.key]: clamp(Number(e.target.value), 0, 100) })}
                      />
                    </div>
                  ))}
                </div>

                {/* Action Buttons */}
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8, marginTop: 16 }}>
                  <button style={styles.ghostBtn} onClick={() => updateOverlay(selected._id, { visible: !selected.visible })}>
                    {selected.visible ? "Hide" : "Show"}
                  </button>
                  <button 
                    style={{...styles.ghostBtn, borderColor: "rgba(239, 68, 68, 0.4)", color: "#fca5a5"}} 
                    onClick={() => deleteOverlay(selected._id)}>
                    Delete
                  </button>
                </div>

                {/* Hint Box */}
                <div style={{ marginTop: 16, padding: "10px 12px", background: "#0f1423", borderRadius: 8, fontSize: 11, color: "#9ca3af", lineHeight: 1.5 }}>
                  <strong>💡 Pro-Tip:</strong> Use arrow keys to nudge, hold Shift to move faster, and press Delete to remove the selected overlay.
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}