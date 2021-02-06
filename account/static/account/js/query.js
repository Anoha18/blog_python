/**
 * Обшая функция запросов
 * @param {string} url адрес по которому отправить запрос
 * @param {RequestInit} opt параметры запроса
 * @returns {Promise<{ error?: string | object, result?: any }>}
 */
const query = async (url, opt) => {
  try {
    const response = await fetch(url, opt);
    if (!response.ok) {
      return { error: 'Error. Произошла ошибка в запросе' };
    }

    const json = await response.json();
    if (json.error) {
      console.error('Error. query.js ', json.error);
    };

    return { result: json.result }
  } catch (error) {
    console.error('Error query.js \nError message = ', error.message);
    return { error };
  }
}

export default query;