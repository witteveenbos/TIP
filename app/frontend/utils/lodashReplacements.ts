/**
 * Custom debounce function to replace lodash.debounce
 * Delays the execution of a function until after a specified delay has passed
 * since the last time it was invoked.
 * 
 * @param func - The function to debounce
 * @param delay - The delay in milliseconds
 * @returns The debounced function with a cancel method
 */
export function debounce<T extends (...args: any[]) => any>(
    func: T,
    delay: number
): T & { cancel: () => void } {
    let timeoutId: NodeJS.Timeout;
    const debouncedFunc = ((...args: Parameters<T>) => {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func(...args), delay);
    }) as T & { cancel: () => void };
    debouncedFunc.cancel = () => {
        clearTimeout(timeoutId);
    };
    return debouncedFunc;
}
/**
 * Custom cloneDeep function to replace lodash/cloneDeep
 * Creates a deep copy of the given object, recursively cloning all nested properties.
 * 
 * @param obj - The object to clone
 * @returns A deep copy of the object
 */
export function cloneDeep<T>(obj: T): T {
    if (obj === null || typeof obj !== 'object') {
        return obj;
    }
    if (obj instanceof Date) {
        return new Date(obj.getTime()) as T;
    }
    if (obj instanceof Array) {
        return obj.map(item => cloneDeep(item)) as T;
    }
    if (typeof obj === 'object') {
        const clonedObj = {} as T;
        for (const key in obj) {
            if (obj.hasOwnProperty(key)) {
                clonedObj[key] = cloneDeep(obj[key]);
            }
        }
        return clonedObj;
    }
    return obj;
}