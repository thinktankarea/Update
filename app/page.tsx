'use client';

import Link from 'next/link';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Header } from '@/components/layout/Header';
import { 
  Search, 
  BarChart3, 
  Calendar, 
  GitCompare, 
  TrendingUp, 
  Shield, 
  Target,
  ArrowRight 
} from 'lucide-react';

export default function HomePage() {
  const tools = [
    {
      title: 'OttoScore™ Viewer',
      description: 'Get detailed analysis and Otto\'s take on any dividend-paying stock or fund',
      icon: BarChart3,
      href: '/score/AAPL',
      color: 'text-blue-600',
      features: ['Score breakdown', 'Factor analysis', 'Otto\'s insights']
    },
    {
      title: 'OttoCore™ Screener',
      description: 'Discover dividend stocks and funds based on your investment criteria',
      icon: Search,
      href: '/screener',
      color: 'text-green-600',
      features: ['Advanced filters', 'Yield ranges', 'Sector screening']
    },
    {
      title: 'Otto3x12™ Calendar',
      description: 'Build monthly income streams using quarterly dividend stocks',
      icon: Calendar,
      href: '/calendar',
      color: 'text-purple-600',
      features: ['Income planning', 'Payment scheduling', 'DRIP simulation']
    },
    {
      title: 'OttoCompare™ Tool',
      description: 'Compare multiple stocks side-by-side with detailed metrics',
      icon: GitCompare,
      href: '/compare',
      color: 'text-orange-600',
      features: ['Side-by-side analysis', 'Factor comparison', 'Decision support']
    }
  ];

  const features = [
    {
      icon: TrendingUp,
      title: 'Quantitative Scoring',
      description: 'Our proprietary OttoScore™ algorithm evaluates dividend stocks across multiple factors'
    },
    {
      icon: Shield,
      title: 'Risk Assessment',
      description: 'Comprehensive analysis of dividend safety, payout ratios, and financial stability'
    },
    {
      icon: Target,
      title: 'Income Planning',
      description: 'Strategic tools for building consistent monthly dividend income streams'
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
            Smart Dividend
            <span className="bg-gradient-to-r from-blue-600 to-teal-600 bg-clip-text text-transparent">
              {' '}Investing
            </span>
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-8">
            OttoTools provides quantitative analysis and strategic planning tools 
            for dividend-focused investors. Make informed decisions with our 
            comprehensive scoring system and portfolio planning features.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/screener">
              <Button size="lg" className="bg-gradient-to-r from-blue-600 to-teal-600 hover:from-blue-700 hover:to-teal-700">
                Start Screening Stocks
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </Link>
            <Link href="/score/AAPL">
              <Button variant="outline" size="lg">
                View Sample Analysis
              </Button>
            </Link>
          </div>
        </div>

        {/* Tools Grid */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-gray-900 text-center mb-12">
            Dividend Investment Tools
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {tools.map((tool) => (
              <Link key={tool.title} href={tool.href}>
                <Card className="h-full hover:shadow-lg transition-all duration-300 cursor-pointer group">
                  <CardHeader>
                    <div className="flex items-center space-x-3 mb-3">
                      <div className={`p-2 rounded-lg bg-gray-50 ${tool.color}`}>
                        <tool.icon className="h-6 w-6" />
                      </div>
                      <CardTitle className="text-xl group-hover:text-blue-600 transition-colors">
                        {tool.title}
                      </CardTitle>
                    </div>
                    <p className="text-gray-600">{tool.description}</p>
                  </CardHeader>
                  <CardContent>
                    <div className="flex flex-wrap gap-2">
                      {tool.features.map((feature) => (
                        <Badge key={feature} variant="secondary">
                          {feature}
                        </Badge>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </Link>
            ))}
          </div>
        </div>

        {/* Features Section */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-gray-900 text-center mb-12">
            Why Choose OttoTools?
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {features.map((feature) => (
              <div key={feature.title} className="text-center">
                <div className="bg-gradient-to-r from-blue-600 to-teal-600 p-3 rounded-full w-16 h-16 mx-auto mb-4 flex items-center justify-center">
                  <feature.icon className="h-8 w-8 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">
                  {feature.title}
                </h3>
                <p className="text-gray-600">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* CTA Section */}
        <Card className="bg-gradient-to-r from-blue-600 to-teal-600 text-white">
          <CardContent className="text-center py-12">
            <h2 className="text-3xl font-bold mb-4">
              Ready to Optimize Your Dividend Portfolio?
            </h2>
            <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
              Join thousands of investors using OttoTools to make smarter 
              dividend investment decisions.
            </p>
            <Link href="/screener">
              <Button size="lg" variant="secondary">
                Get Started Free
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </Link>
          </CardContent>
        </Card>
      </main>
    </div>
  );
}