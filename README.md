# Casa de Leilões — Verzel

Projeto desenvolvido para o desafio técnico da Verzel, com React, FastAPI, PostgreSQL e SQLAlchemy.

## Acesso

- Site: https://projeto-leilao-five.vercel.app
- Documentação da API: https://projeto-leilao.onrender.com/docs

## Funcionalidades

- Login com JWT.
- Busca de obras, criação e cancelamento de leilões.
- Lances em tempo real com WebSocket.
- Carteira com depósito e reserva de saldo.
- Encerramento automático e liquidação.
- Histórico, comprovante e auditoria com SHA-256.

## Contas de demonstração

| E-mail | Perfil |
|---|---|
| joao@example.com | Leiloeiro |
| carlos@example.com | Licitante |
| maria@example.com | Licitante |

Senha de todas as contas: `Teste12345`

## Uso de IA

Utilizei IA para aprender e implementar autenticação com JWT e WebSocket, tecnologias com as quais ainda não havia trabalhado. Também utilizei assistência na estilização, resolução de bugs e validação de fuso horário com `datetime.utcoffset()`.

## Hospedagem

Frontend na Vercel, backend no Render e banco no Neon.

O backend gratuito pode demorar no primeiro acesso após ficar inativo. Durante a suspensão, o worker também pausa; os encerramentos pendentes são processados quando o serviço volta a executar.

## Disponibilidade

A demonstração ficará disponível por 30 dias a partir da entrega do desafio.
