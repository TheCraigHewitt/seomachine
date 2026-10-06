"use client";
// Live mic via the Web Speech API. Chrome/Edge/Safari support it; Firefox falls back to typing.
import { useCallback, useEffect, useRef, useState } from "react";

/* eslint-disable @typescript-eslint/no-explicit-any */
type Recognition = any;

export function useMic(onFinal: (text: string) => void, onInterimObjection?: (text: string) => void) {
  const [supported, setSupported] = useState(false);
  const [listening, setListening] = useState(false);
  const [interim, setInterim] = useState("");
  const [error, setError] = useState<string | null>(null);
  const rec = useRef<Recognition | null>(null);
  const buffer = useRef("");
  const finalCb = useRef(onFinal);
  const objCb = useRef(onInterimObjection);
  finalCb.current = onFinal;
  objCb.current = onInterimObjection;

  useEffect(() => {
    const SR = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SR) return;
    setSupported(true);
    const r: Recognition = new SR();
    r.continuous = true;
    r.interimResults = true;
    r.lang = "en-US";
    r.onresult = (e: any) => {
      let live = "";
      for (let i = e.resultIndex; i < e.results.length; i++) {
        const res = e.results[i];
        if (res.isFinal) buffer.current += res[0].transcript + " ";
        else live += res[0].transcript;
      }
      const shown = (buffer.current + live).trim();
      setInterim(shown);
      // Let the courtroom react instantly when counsel shouts "Objection".
      if (/\bobjection\b/i.test(live) || /\bobjection\b/i.test(buffer.current)) objCb.current?.(shown);
    };
    r.onerror = (e: any) => { if (e.error !== "no-speech" && e.error !== "aborted") setError(e.error); };
    r.onend = () => setListening(false);
    rec.current = r;
    return () => r.abort();
  }, []);

  const start = useCallback(() => {
    if (!rec.current || listening) return;
    buffer.current = "";
    setInterim("");
    setError(null);
    try { rec.current.start(); setListening(true); } catch { /* already started */ }
  }, [listening]);

  /** Stops listening and submits what was heard. */
  const stop = useCallback(() => {
    if (!rec.current) return;
    rec.current.stop();
    setListening(false);
    setTimeout(() => {
      const text = (buffer.current || "").trim() || interimRef.current.trim();
      buffer.current = "";
      setInterim("");
      if (text) finalCb.current(text);
    }, 350);
  }, []);

  const interimRef = useRef("");
  interimRef.current = interim;

  const cancel = useCallback(() => { rec.current?.abort(); buffer.current = ""; setInterim(""); setListening(false); }, []);

  return { supported, listening, interim, error, start, stop, cancel };
}
