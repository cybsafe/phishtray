import React, { useEffect, useState } from 'react';
import { HOST_BACKEND } from '../../utils';

const useFetch = (url, options) => {
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch(url, options);
        await setLoading(true);
        const json = await res.json();
        await setLoading(false);
        setResponse(json);
      } catch (error) {
        setError(error);
      }
    };
    fetchData();
  }, []);
  return { response, error, loading };
};

function Debrief({
  match: {
    params: { participantUuid },
  },
}) {
  const apiUrl = `${HOST_BACKEND}/api/v1/participant-scores/${participantUuid}`;

  const data = useFetch(apiUrl, null);

  if (data.loading) {
    return 'loading';
  }

  return (
    <div>
      {console.log(data)}
      {<div>Debrief</div>}
    </div>
  );
}

export default Debrief;
