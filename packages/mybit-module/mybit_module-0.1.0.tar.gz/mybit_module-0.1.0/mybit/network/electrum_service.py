from mybit.network.electrum_client import ElectrumClient

class ElectrumService(ElectrumClient):
    def __init__(self, host, port, proto):
        """
        Inicializa la clase ElectrumBase llamando al constructor de la clase base 
        ElectrumClient e inicializa el cliente con los parámetros host, port y proto.
        
        :param host: Dirección del servidor Electrum.
        :param port: Puerto del servidor Electrum.
        :param proto: Protocolo utilizado para la conexión (e.g., 'tcp' o 'ssl').
        """
        super().__init__(host, port, proto)

    def validate_response(self, response):
        if not response or 'error' in response:
            raise ValueError(f"Invalid response from server: {response}")
        return response

    def get_server_version(self):
        """
        Envía una solicitud al servidor para obtener la versión del servidor Electrum.
        
        :return: La versión del servidor Electrum.
        """
        response = self.send_request('server.version')
        return self.validate_response(response)

    def get_utxos(self, address_script_hash):
        """
        Obtiene los UTXOs (Unspent Transaction Outputs) asociados a una dirección, 
        utilizando el script_hash de la dirección.

        :param address_script_hash: El script_hash de la dirección.
        :return: Lista de UTXOs asociados a la dirección.
        """
        response = self.send_request('blockchain.scripthash.listunspent', [address_script_hash])
        return self.validate_response(response)['result']
    
    def get_unconfirmed_transactions(self, address_script_hash):
        """
        Obtiene las transacciones no confirmadas (en el mempool) asociadas a una dirección, 
        utilizando el script_hash de la dirección.
        
        :param address_script_hash: El script_hash de la dirección.
        :return: Lista de transacciones no confirmadas.
        """
        response = self.send_request('blockchain.scripthash.get_mempool', [address_script_hash])
        return self.validate_response(response)['result']
    
    def get_confirmed_utxos(self, address_script_hash):
        """
        Obtiene los UTXOs (Unspent Transaction Outputs) confirmados asociados a una dirección,
        filtrando aquellos que están relacionados con transacciones no confirmadas.

        :param address_script_hash: El script_hash de la dirección.
        :return: Lista de UTXOs confirmados asociados a la dirección.
        """
        utxos_filtered = []

        get_utxos = self.get_utxos(address_script_hash)
        get_unconfirmed_transactions = self.get_unconfirmed_transactions(address_script_hash)
        unconfirmed_tx_hashes = [tx['tx_hash'] for tx in get_unconfirmed_transactions]

        if not len(get_utxos) > 0:
            return []

        for utxo in get_utxos:
            if not utxo['tx_hash'] in unconfirmed_tx_hashes:
                utxos_filtered.append(utxo)
        
        return utxos_filtered
    
    def get_filtered_utxos(self, address_script_hash, min_confirmations=3):
        """
        Obtiene los UTXOs confirmados que tienen al menos un número mínimo de confirmaciones,
        utilizando la lista de UTXOs confirmados filtrados por la función `get_confirmed_utxos`.

        :param address_script_hash: El script_hash de la dirección.
        :param min_confirmations: El número mínimo de confirmaciones requeridas (por defecto es 3).
        :return: Lista de UTXOs con el número mínimo de confirmaciones asociadas a la dirección.
        """
        get_utxos = self.get_confirmed_utxos(address_script_hash)

        if not get_utxos:
            return []

        utxos_filtered = []
        for utxo in get_utxos:
            tx_hash = utxo['tx_hash']
            get_confirmations = self.get_transaction_confirmations(tx_hash)

            if get_confirmations >= min_confirmations:
                utxo['confirmations'] = get_confirmations
                utxos_filtered.append(utxo)  # Solo añadir los UTXOs que cumplen la condición

        return utxos_filtered
    
    def get_address_balance(self, address_script_hash):
        """
        Obtiene el balance asociado a una dirección, utilizando el script_hash de la dirección.
        
        :param address_script_hash: El script_hash de la dirección.
        :return: El balance de la dirección.
        """
        response = self.send_request('blockchain.scripthash.get_balance', [address_script_hash])
        return self.validate_response(response)
    
    def get_address_history(self, address_script_hash):
        """
        Obtiene el historial de transacciones asociadas a una dirección, utilizando el script_hash de la dirección.
        
        :param address_script_hash: El script_hash de la dirección.
        :return: El historial de transacciones de la dirección.
        """
        response = self.send_request('blockchain.scripthash.get_history', [address_script_hash])
        return self.validate_response(response)
    
    def get_transaction_details(self, txid):
        """
        Obtiene los detalles de una transacción específica utilizando el ID de la transacción (txid).
        
        :param txid: El ID de la transacción.
        :return: Detalles de la transacción.
        """
        response = self.send_request('blockchain.transaction.get', [txid, True])
        return response
    
    def get_current_block_height(self):
        """
        Obtiene la altura del bloque actual al suscribirse a los encabezados de los bloques.
        
        :return: La altura del bloque actual.
        """
        height = self.send_request('blockchain.headers.subscribe')
        return height['result'].get('height', None)
    
    def get_block_header_by_blockhash(self, blockhash):
        """
        Obtiene el encabezado de un bloque específico utilizando su hash.
        
        :param blockhash: El hash del bloque.
        :return: Encabezado del bloque.
        """
        response = self.send_request('blockchain.block.header', [blockhash])
        return response
    
    def get_block_header_by_height(self, height: int):
        """
        Obtiene el encabezado de un bloque específico utilizando su altura.
        
        :param height: La altura del bloque.
        :return: Encabezado del bloque.
        """
        response = self.send_request('blockchain.block.header', [height])
        return self.validate_response(response)

    def send_transaction(self, tx_hex):
        """
        Envía una transacción a la red utilizando el hex de la transacción.
        
        :param tx_hex: El hex de la transacción.
        :return: Resultado de la difusión de la transacción.
        """
        response = self.send_request('blockchain.transaction.broadcast', [tx_hex])
        return self.validate_response(response)
    
    def get_transaction_merkle(self, txid):
        """
        Obtiene el Merkle proof de una transacción específica utilizando su txid.
        
        :param txid: El ID de la transacción.
        :return: Prueba de Merkle de la transacción.
        """
        response = self.send_request('blockchain.transaction.get_merkle', [txid])
        return self.validate_response(response)
    
    def get_estimate_fee(self, block_confirmations_fee: int = 2):
        """
        Obtiene una estimación de la comisión necesaria para que una transacción sea confirmada 
        en un número determinado de bloques (por defecto, 2 bloques).
        
        :param block_confirmations_fee: El número de bloques para la confirmación estimada.
        :return: Estimación de la comisión en BTC/kB.
        """
        response = self.send_request('blockchain.estimatefee', [block_confirmations_fee])
        return self.validate_response(response)
    
    def get_transaction_confirmations(self, txid):
        """
        Obtiene el número de confirmaciones de una transacción utilizando su txid.
        
        :param txid: El ID de la transacción.
        :return: Número de confirmaciones de la transacción.
        """
        # Obtiene la altura del bloque donde se incluyó la transacción.
        get_transaction_height = self.get_transaction_merkle(txid)

        # Verifica si el método 'blockchain.transaction.get_merkle' es soportado y devuelve un resultado.
        if not get_transaction_height.get('result'):
            raise('fail to get transactions confirmations - [blockchain.transaction.get_merkle] method not supported')
        
        # Extrae la altura del bloque de la respuesta.
        block_height = get_transaction_height['result'].get('block_height', None)
        
        # Si no hay altura de bloque (es decir, la transacción aún está en el mempool), 
        # se considera que no tiene confirmaciones.
        if block_height is None:
            return 0  # Transacción aún no confirmada (en el mempool)
        
        # Obtiene la altura del bloque actual.
        current_block_height = self.get_current_block_height()

        # Calcula el número de confirmaciones restando la altura del bloque de la transacción 
        # de la altura actual del bloque, y sumando 1 (para incluir la primera confirmación).
        confirmations = current_block_height - block_height + 1
        return confirmations