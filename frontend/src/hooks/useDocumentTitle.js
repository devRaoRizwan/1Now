import { useEffect } from "react";
import { APP_NAME } from "../constants/navigation.js";

export function useDocumentTitle(title) {
  useEffect(() => {
    document.title = title ? `${title} · ${APP_NAME} | 1Now` : `${APP_NAME} | 1Now`;
  }, [title]);
}
