import { useCallback, useEffect, useState } from "react";

// Loads data whenever `deps` change and ignores responses that arrive after a newer request.
export function useFetch(load, deps) {
  const [state, setState] = useState({ data: null, error: null });

  useEffect(() => {
    let active = true;
    load()
      .then((data) => active && setState({ data, error: null }))
      .catch((error) => active && setState({ data: null, error: error.message }));
    return () => {
      active = false;
    };
  }, deps);

  const setData = useCallback((data) => setState({ data, error: null }), []);
  return { ...state, setData };
}
