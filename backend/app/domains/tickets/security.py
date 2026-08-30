async def validate_at_gate(self, code: str, session_id: uuid.UUID) -> TicketValidationResult:
        try:
            payload = decode_ticket_payload(code)
        except ValueError:
            return TicketValidationResult(result="invalid", message="QR inválido, corrompido ou forjado")

        ticket_id = uuid.UUID(payload["ticket_id"])
        
        # Busca o ticket aplicando o LOCK PESSIMISTA (com for update)
        ticket = await self.ticket_repo.get_by_id_for_update(ticket_id)

        if ticket is None:
            return TicketValidationResult(result="invalid", message="Ingresso não encontrado")

        if str(session_id) != payload["session_id"]:
            return TicketValidationResult(result="wrong_event", message="Ingresso não é desta sessão/evento")

        if ticket.status == TicketStatus.USED:
            return TicketValidationResult(result="already_used", message="Ingresso já foi utilizado")

        # Atualiza de forma atômica
        ticket.status = TicketStatus.USED
        await self.ticket_repo.persist(ticket)

        return TicketValidationResult(result="valid", message="Ingresso válido! Entrada liberada")