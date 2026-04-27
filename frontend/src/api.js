import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

export const generateNotes = async (url) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/notes`, {
            params: { url }
        });
        return response.data;
    } catch (error) {
        if (error.response && error.response.data) {
            throw new Error(error.response.data.error || error.response.data.detail || 'Server error occurred');
        }
        throw new Error(error.message);
    }
};
