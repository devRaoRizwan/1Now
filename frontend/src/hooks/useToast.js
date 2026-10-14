import { useCallback, useEffect, useRef, useState } from "react";

export function useToast(duration = 3000) {
  const [message, setMessage] = useState(null);
  const timer = useRef(null);

  const notify = useCallback(
    (text) => {
      clearTimeout(timer.current);
      setMessage(text);
      timer.current = setTimeout(() => setMessage(null), duration);
    },
    [duration],
  );

  useEffect(() => () => clearTimeout(timer.current), []);

  return { message, notify };
}
