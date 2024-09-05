const submit = async (endpoint, data, formData = null) => {
    try {
      const requestOptions = {
        method: 'POST',
        headers: {},
        body: formData ? formData : JSON.stringify(data),
      };
  
      if (!formData) {
        requestOptions.headers['Content-Type'] = 'application/json';
      }
  
      const response = await fetch(endpoint, requestOptions);
      const responseData = await response.json();
      return responseData;
    } catch (error) {
      console.error('Error making POST request:', error);
      throw error;
    }
  };
 

const ask = async (data) => {
    if (data && data.length > 0) {
        const endpoint = 'http://localhost:5000/ask';
        const response = await submit(endpoint, {"question":data});
        
        if (response) {
          return response["answer"]
        }
    }
}

const upload = async (file) => {
    if (file) {
        const endpoint = 'http://localhost:5000/upload';
        const formData = new FormData();
        formData.append('file', file);
        return submit(endpoint, null, formData);
    }
}

export { ask, upload };
