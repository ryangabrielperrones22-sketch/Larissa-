import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const authHeader = request.headers.get('authorization')
  
  if (!authHeader) {
    return new NextResponse('Autenticação necessária', {
      status: 401,
      headers: {
        'WWW-Authenticate': 'Basic realm="Acesso Restrito"',
      },
    })
  }

  const base64 = authHeader.split(' ')[1]
  const [user, pass] = Buffer.from(base64, 'base64').toString().split(':')
  
  // 👇 MUDE AQUI o usuário e senha que você quer
  const validUser = 'cliente1'
  const validPass = 'senha123'

  if (user === validUser && pass === validPass) {
    return NextResponse.next()
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
  matcher: '/(.*)',
}