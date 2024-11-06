# gcair/get_sim_params.py

async def get_sim_params () -> str:
    """ 获取gc air 用户的 token"""
    code = """
        (async function() {
            return new Promise((resolve, reject) => {
                const request = indexedDB.open("JupyterLite Storage");

                request.onsuccess = (event) => {
                    const db = event.target.result;
                    const transaction = db.transaction("files", "readonly");
                    const store = transaction.objectStore("files");
                    const getAllRequest = store.getAll();

                    getAllRequest.onsuccess = () => {
                        resolve(getAllRequest.result);
                    };

                    getAllRequest.onerror = (error) => {
                        reject(error);
                    };
                };

                request.onerror = (error) => {
                    reject(error);
                };
            });
        })();
        """
    result = await eval(code)

    return result