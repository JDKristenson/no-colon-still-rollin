import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '@/contexts/AuthContext'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { motion } from 'framer-motion'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    try {
      await login(email, password)
      navigate('/dashboard')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-md"
      >
        <Card className="shadow-xl border-0">
          <CardHeader className="space-y-1">
            <div className="flex items-center justify-center gap-4">
              <svg
                width="48"
                height="64"
                viewBox="0 0 120 160"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
                className="flex-shrink-0"
              >
                {/* Drop shadow */}
                <g filter="url(#shadow)">
                  <path
                    d="M60 15 L60 145"
                    stroke="#1e3a8a"
                    strokeWidth="5"
                    strokeLinecap="round"
                    opacity="0.3"
                    transform="translate(2, 2)"
                  />
                </g>
                {/* Rod of Asclepius - Staff (vertical staff) */}
                <path
                  d="M60 15 L60 145"
                  stroke="#1e3a8a"
                  strokeWidth="5"
                  strokeLinecap="round"
                />
                {/* Snake - Complete body with three distinct coils wrapping around staff */}
                <path
                  d="M38 28 Q35 30 38 32 L38 35 Q35 38 35 42 Q35 48 42 52 Q50 56 50 62 Q50 68 58 72 Q68 76 68 82 Q68 88 58 92 Q48 96 42 100 Q35 104 35 110 Q35 116 42 120 Q50 124 52 130 Q52 134 50 138"
                  stroke="#1e3a8a"
                  strokeWidth="4"
                  fill="none"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                {/* Snake head (upper left, facing right) - more defined */}
                <path
                  d="M38 25 Q35 22 32 25 Q30 27 32 29 Q35 31 38 29"
                  stroke="#1e3a8a"
                  strokeWidth="4"
                  fill="#1e3a8a"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                {/* Snake eye (small white dot) */}
                <circle cx="35" cy="26" r="1.5" fill="white" />
                <defs>
                  <filter id="shadow" x="-50%" y="-50%" width="200%" height="200%">
                    <feGaussianBlur in="SourceAlpha" stdDeviation="2"/>
                    <feOffset dx="2" dy="2" result="offsetblur"/>
                    <feComponentTransfer>
                      <feFuncA type="linear" slope="0.3"/>
                    </feComponentTransfer>
                    <feMerge>
                      <feMergeNode/>
                      <feMergeNode in="SourceGraphic"/>
                    </feMerge>
                  </filter>
                </defs>
              </svg>
              <CardTitle className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                No Colon, Still Rollin'
              </CardTitle>
            </div>
            <CardDescription className="text-center">
              Sign in to continue your journey
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              {error && (
                <div className="p-3 text-sm text-red-600 bg-red-50 rounded-md">
                  {error}
                </div>
              )}
              <div className="space-y-2">
                <label htmlFor="email" className="text-sm font-medium">
                  Email
                </label>
                <Input
                  id="email"
                  type="email"
                  placeholder="you@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
              <div className="space-y-2">
                <label htmlFor="password" className="text-sm font-medium">
                  Password
                </label>
                <Input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>
              <Button type="submit" className="w-full" size="lg">
                Sign In
              </Button>
              <div className="text-center text-sm">
                <span className="text-muted-foreground">Don't have an account? </span>
                <Link to="/register" className="text-primary hover:underline">
                  Sign up
                </Link>
              </div>
            </form>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  )
}

