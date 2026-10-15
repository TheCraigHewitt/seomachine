"use client";
import { useState } from "react";
import { useMic } from "@/lib/speech/useMic";

interface Props {
  onSubmit: (text: string) => void;
  onObjectionHeard: () => void;
  disabled: boolean;
  placeholder: string;
}

/** The player's podium: push-to-talk mic with a typed fallback. */
export default function Lectern({ onSubmit, onObjectionHeard, disabled, placeholder }: Props) {
  const [text, setText] = useState("");
  const mic = useMic(onSubmit, onObjectionHeard);

  const send = () => { if (text.trim()) { onSubmit(text.trim()); setText(""); } };

  return (
    <div className="panel p-3">
      <div className="flex items-center gap-3">
        {mic.supported ? (
          <button
            disabled={disabled}
            onClick={mic.listening ? mic.stop : mic.start}
            className={`flex h-14 w-14 shrink-0 items-center justify-center rounded-full text-2xl transition ${mic.listening ? "mic-live bg-guilty text-white" : "bg-brass text-wood-950 hover:brightness-110"} disabled:opacity-40`}
            aria-label={mic.listening ? "Stop and submit" : "Start speaking"}
            title={mic.listening ? "Click to finish speaking (or press Enter)" : "Click to speak"}
          >
            {mic.listening ? "■" : "🎙"}
          </button>
        ) : (
          <div className="w-14 shrink-0 text-center text-[10px] text-ink">Mic needs Chrome, Edge or Safari</div>
        )}
        <div className="flex-1">
          {mic.listening ? (
            <div className="min-h-14 rounded-md border border-guilty/50 bg-wood-950 p-2 text-sm">
              <span className="mr-2 text-xs font-semibold text-guilty">● LIVE</span>
              {mic.interim || <span className="text-ink">Listening… speak to the court.</span>}
            </div>
          ) : (
            <textarea
              value={text}
              disabled={disabled}
              onChange={(e) => setText(e.target.value)}
              onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); } }}
              rows={2}
              placeholder={placeholder}
              className="w-full resize-none rounded-md border border-wood-600 bg-wood-950 p-2 text-sm outline-none focus:border-brass disabled:opacity-50"
            />
          )}
        </div>
        {!mic.listening && (
          <button onClick={send} disabled={disabled || !text.trim()} className="brass-btn shrink-0">Speak</button>
        )}
      </div>
      {mic.error && <p className="mt-1 text-xs text-guilty">Mic error: {mic.error}. Check browser mic permissions, or type instead.</p>}
    </div>
  );
}
