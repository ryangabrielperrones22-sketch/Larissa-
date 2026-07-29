import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // Pega a autenticação enviada pelo navegador
  const authHeader = request.headers.get('authorization')
  
  if (!authHeader) {
    // Se não enviou login, pede autenticação
    return new NextResponse('Autenticação necessária', {
      status: 401,
      headers: {
        'WWW-Authenticate': 'Basic realm="Acesso Restrito"',
      },
    })
  }

  // Decodifica o usuário e senha (Basic Auth)
  const base64 = authHeader.split(' ')[1]
  const [user, pass] = Buffer.from(base64, 'base64').toString().split(':')
  
  // Pega as credenciais das variáveis de ambiente
  const validUser = process.env.AUTH_USER
  const validPass = process.env.AUTH_PASS

  if (user === validUser && pass === validPass) {
    return NextResponse.next() // Libera o acesso
  } else {
    return new NextResponse('Credenciais inválidas', {
      status: 401,
      headers: {
        'WWW-Authenticate': 'Basic realm="Acesso Restrito"',
      },
    })
  }
}

export const config = {
  matcher: '/(.*)', // Protege todas as páginas
}