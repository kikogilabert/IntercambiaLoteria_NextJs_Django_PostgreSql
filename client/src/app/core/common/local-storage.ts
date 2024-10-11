import { StorageVariables } from "@core/constants";

export const CustomStorage = {
    "getItem": <T>(id: StorageVariables): (T | null) => {
        if (typeof window !== 'undefined') {
            try {
                return JSON.parse(localStorage.getItem(id) as string) as T
            } catch (e) { }
            return localStorage.getItem(id) as T
        } else {
            return null
        }
    },
    "removeItem": (id: StorageVariables): boolean => {
        if (typeof window !== 'undefined') {
            localStorage.removeItem(id)
            return true
        }
        return false;

    },
    "setItem": <T>(id: StorageVariables, value: T): boolean => {
        if (typeof window !== 'undefined') {
            try {
                localStorage.setItem(id, ((typeof value === 'string') ? value : JSON.stringify(value)))
            } catch (e) {
                return false
            }
            return true
        }
        return false;
    }
}