class UTXOSelector:
    # Costos típicos de inputs y outputs en bytes
    COST_PER_INPUT_LEGACY = 148  # Bytes para input estándar (no-SegWit)
    COST_PER_INPUT_SEGWIT = 67   # Bytes para input SegWit
    COST_PER_OUTPUT = 34         # Bytes para output
    COST_OVERHEAD_LEGACY = 8     # Overhead típico para transacciones legacy
    COST_OVERHEAD_SEGWIT = 10    # Overhead típico para transacciones SegWit
    DEFAULT_FEE_PER_BYTE = 1     # Tarifa por byte en satoshis si no se especifica

    def __init__(self, fee_per_byte=None):
        self.fee_per_byte = fee_per_byte or self.DEFAULT_FEE_PER_BYTE

    @staticmethod
    def calculate_fee(selected_utxos, num_outputs, is_segwit, fee_per_byte):
        """Calcula el tamaño estimado de la transacción en bytes y la tarifa correspondiente."""
        total_input_size = sum(UTXOSelector.COST_PER_INPUT_SEGWIT if utxo.segwit else UTXOSelector.COST_PER_INPUT_LEGACY for utxo in selected_utxos)
        total_output_size = num_outputs * UTXOSelector.COST_PER_OUTPUT
        overhead = UTXOSelector.COST_OVERHEAD_SEGWIT if is_segwit else UTXOSelector.COST_OVERHEAD_LEGACY
        total_size = total_input_size + total_output_size + overhead
        return total_size * fee_per_byte

    def branch_and_bound(self, utxos, target, num_outputs=1):
        """Implementación de la selección de UTXOs usando el algoritmo Branch and Bound."""
        # Ordenar UTXOs de mayor a menor por valor
        utxos = sorted(utxos, key=lambda x: x.amount, reverse=True)
        
        # Determinar si la transacción tiene UTXOs SegWit
        is_segwit = any(utxo.segwit for utxo in utxos)
        
        def bound(index, current_sum, estimated_fee):
            """Verifica si se debe continuar explorando esta rama."""
            if current_sum >= target + estimated_fee:
                return True
            if index >= len(utxos):
                return False
            new_estimated_fee = self.calculate_fee(utxos[:index + 1], num_outputs, is_segwit, self.fee_per_byte)
            return bound(index + 1, current_sum + utxos[index].amount, new_estimated_fee) or bound(index + 1, current_sum, estimated_fee)

        def search(index, current_sum, selected, estimated_fee):
            """Explora las combinaciones posibles de UTXOs."""
            if current_sum >= target + estimated_fee:
                return selected
            if index >= len(utxos) or not bound(index, current_sum, estimated_fee):
                return None

            # Opción 1: Seleccionamos este UTXO
            new_estimated_fee = self.calculate_fee(selected + [utxos[index]], num_outputs, is_segwit, self.fee_per_byte)
            selected_with = search(index + 1, current_sum + utxos[index].amount, selected + [utxos[index]], new_estimated_fee)
            
            # Opción 2: No seleccionamos este UTXO
            selected_without = search(index + 1, current_sum, selected, estimated_fee)

            if selected_with and (selected_without is None or len(selected_with) < len(selected_without)):
                return selected_with
            return selected_without

        selected_utxos = search(0, 0, [], 0)
        
        if not selected_utxos:
            return None, 0, 0  # No se encontraron suficientes UTXOs

        # Calculamos el costo total en tarifas
        total_fee = self.calculate_fee(selected_utxos, num_outputs, is_segwit, self.fee_per_byte)
        total_utxo_value = sum(utxo.amount for utxo in selected_utxos)
        total_change = total_utxo_value - (target + total_fee)

        # Si el cambio es menor que 0 o el fee es mayor a la cantidad de los utxos, no es posible realizar la transacción
        if (total_change < 0) or (total_fee > total_utxo_value):
            return selected_utxos, total_fee, None 

        if total_change >= self.COST_PER_OUTPUT:
            num_outputs_with_change = num_outputs + 1
            total_fee_with_change = self.calculate_fee(selected_utxos, num_outputs_with_change, is_segwit, self.fee_per_byte)
            total_change = total_utxo_value - (target + total_fee_with_change)
            
            if total_change < 0:
                total_fee += total_utxo_value - (target + total_fee)  # Agregar el cambio sobrante al fee
                total_change = 0
            else:
                total_fee = total_fee_with_change
        else:
            # Si el cambio es menor que el costo de un nuevo output, sumamos el cambio al fee
            total_fee += total_change
            total_change = 0

        return selected_utxos, total_fee, total_change